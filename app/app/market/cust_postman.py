from postman.views import WriteView, ReplyView, MessageView, ConversationView
from app.market.forms import MarketWriteForm, MarketFullReplyForm, MarketQuickReplyForm
from postman.models import Message
from django.db.models import Q

class MyConv(ConversationView):
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
        context = super(MyConv, self).get_context_data(**kwargs)
        context.update({
            'by_conversation': True,
        })
        return context


