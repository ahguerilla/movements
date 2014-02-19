from celery import shared_task, task
from app.users.models import UserProfile
from app.market.models import MarketItem,Notification
from django.db.models import Q
import json

if not '_app' in dir():
    from celery import Celery
    _app = Celery('celerytasks',broker='amqp://guest@localhost//')


def get_notification_text(obj, update=False):    
    return json.dumps({
        'update':update,
        'title': obj.title
    })


def get_notification_comment_text(obj, username, comment, not_yours=False):
    return json.dumps({
        'username': username,
        'title': obj.title,
        'comment':comment.id,
        'not_yours': not_yours
    })

   
def find_people_interested_in(obj):
    skills = [skill.id for skill in obj.skills.all()]
    countries = [country.id for country in obj.countries.all()]
    issues = [issue.id for issue in obj.issues.all()]
    query = Q(skills__in=skills) | Q(issues__in=issues) | Q(countries__in=countries)
    query = query & ~Q(user=obj.owner) 
    profiles = UserProfile.objects.filter(query).distinct('id').only('user').all()
    return profiles


@shared_task
@_app.task(name="createNotification", bind=True)
def create_notification(self,obj):
    notifications = [ notif.user for notif in Notification.objects.filter(item=obj.id).only('user').all()]    
    profiles = find_people_interested_in(obj)
    for profile in profiles:
        if profile.user.id in notifications:
            continue
        notification = Notification()
        notification.user = profile.user
        notification.item = obj
        notification.avatar_user = obj.owner.username
        notification.text = get_notification_text(obj)
        notification.save()
    return


@shared_task
@_app.task(name="createCommentNotification", bind=True)
def create_comment_notification(self,obj,comment,username):    
    created = []
    if obj.owner.username != username:
        notification = Notification()
        notification.user = obj.owner
        notification.item = obj
        notification.avatar_user = username
        notification.comment_id = comment.id
        notification.text = get_notification_comment_text(obj,username,comment)    
        notification.save()    
        created.append(obj.owner.id)
    for cmnt in obj.comments.all():        
        if cmnt.owner.username != username and cmnt.owner.id not in created and cmnt.deleted==False:
            notification = Notification()
            notification.user = cmnt.owner
            notification.item = obj
            notification.avatar_user = username
            notification.comment_id = comment.id
            notification.text = get_notification_comment_text(obj,username,comment,True)    
            notification.save()            
            created.append(cmnt.owner.id)    
    return


@shared_task
@_app.task(name="updateNotifications", bind=True)
def update_notifications(self,obj):
    notification_objs = Notification.objects.filter(item=obj.id).only('user','read').all()
    notification_userids =set(notification.user.id for notification in notification_objs )
    profiles = find_people_interested_in(obj)
    user_ids = set(profile.user.id for profile in profiles)    

    notifications_tocereate=user_ids.difference(notification_userids)    
    for user_id in notifications_tocereate:        
        notification = Notification()
        notification.user_id = user_id
        notification.item = obj
        notification.avatar_user = obj.owner.username
        notification.text = get_notification_text(obj)
        notification.save()

    notifications_toupdate = user_ids.intersection(notification_userids)    
    for user_id in notifications_toupdate:        
        notification = Notification()
        notification.user_id = user_id
        notification.item = obj
        notification.avatar_user = obj.owner.username
        notification.text = get_notification_text(obj,update=True)
        notification.save()                        
    return


@shared_task
@_app.task(name="markReadNotifications", bind=True)
def mark_read_notifications(self, obj_ids, user_id):    
    notifications = Notification.objects.filter(user=user_id).filter(item__in=obj_ids).filter(read=False).update(read=True)    
    return
