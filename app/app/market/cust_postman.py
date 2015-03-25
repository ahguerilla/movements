from django.db.models import Q
from django.http import Http404

from postman.forms import FullReplyForm
from postman.views import ConversationView
from postman.models import Message

from app.celerytasks import new_postman_message


class MovementsReplyForm(FullReplyForm):
    def save(self, *args, **kwargs):
        is_success = super(MovementsReplyForm, self).save(*args, **kwargs)
        if is_success:
            new_postman_message.delay(self.instance)
        return is_success


class MovementsConversationView(ConversationView):
    def get(self, request, thread_id, *args, **kwargs):
        user = request.user
        self.filter = Q(thread=thread_id)
        self.msgs = Message.objects.thread(user, self.filter).order_by('-sent_at')
        if not self.msgs:
            raise Http404
        Message.objects.set_read(user, self.filter)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(MovementsConversationView, self).get_context_data(**kwargs)
        context.update({
            'by_conversation': True,
        })
        return context
