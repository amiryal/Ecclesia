from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import gettext_lazy as _
from django.core import urlresolvers
from groups.models import GroupProfile
from common.models import Presentable
from common.utils import get_domain

class SpeechAct(models.Model):
    """
    Abstract class for different kinds of speech acts.
    """

    story = models.TextField(_('story'), help_text=_("The user content"))
    created_by = models.ForeignKey(User,
                                   editable=False,
                                   verbose_name=_('created by'),
                                   null=True,
                                   blank=True,
                                   help_text=
                                   _('The user that made the speech')
                                  )
    created_at = models.DateTimeField(_('created at'),
                                      auto_now_add=True,
                                      help_text=_('When the speech was made')
                                     )
    updated_at = models.DateTimeField(_('updated at'),
                                      auto_now=True,
                                      help_text=
                                      _('When the speech was last updated')
                                     )
    
    class Meta:
        verbose_name = _('story')
        verbose_name_plural = _('stories')
    
    def get_absolute_url(self):
        return urlresolvers.reverse('admin:discussion_story_change', args=(self.id,))
    
    def __unicode__(self):
        format = _("%(user)s's %(speechact)s (#%(id)s)")
        return format % {'user':self.created_by.get_full_name(),
                         'speechact':self.Meta.verbose_name,
                         'id':self.id
                        }

    def name_with_link(self):
        return _('<a href="%(url)s">%(user)s\'s %(speechact)s (#%(id)s)</a>') % {'user':self.created_by.get_full_name(), 'speechact':self.get_speech_act_display(), 'id':self.id, 'url':self.get_absolute_url()}

class DiscussionType(models.Model):
    name = models.CharField(_('name'), max_length=50, help_text=_('The name of the discussion type.'))
		
class Discussion(Presentable):
    """
    A discussion between users, related to a group
    """
    group = models.ForeignKey(GroupProfile, verbose_name=_('group profile'), related_name='discussions', help_text=_("The group profile containing this discussion."))
    name = models.CharField(_('name'), max_length=50, help_text=_('The name of the discussion.'))
    slug = models.SlugField(_('slug'), help_text=_("The url representation of the discussion's name. No whitespaces allowed - use hyphen/underscore to separate words"))
    type = models.ForeignKey(DiscussionType, verbose_name=_('discussion type'), related_name='objects', help_text=_("The discussion's type."))
    description = models.CharField(_('short description'), max_length=500, null=True, blank=True, help_text=_('A short description of the discussion.'))
    # no nesting on this release...
	#parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', null=True, blank=True, help_text=_('The parent discussion containing this discussion.'))
    # keeping it simple...
    #forked_from = models.ForeignKey('self', verbose_name=_('forked from'), related_name='forks', null=True, blank=True, help_text=_('The discussion from which this discussion forked.'))
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that created the discussion.'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When was the discussion created.'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When was the discussion last updated.'))

    class Meta:
        verbose_name = _('discussion')
        verbose_name_plural = _('discussions')
        
    
    def get_absolute_url(self):
        return "http://%s/%s/discussion/%s/" % (get_domain(), self.group.slug, self.slug)
    
    def __unicode__(self):
        return self.name
