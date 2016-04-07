from . import views as feebacks_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/feedbacks',feebacks_views.FeedbackViewSet)
router.register(r'api/feedbackcategory',feebacks_views.FeedbackCategoryViewSet)
router.register(r'api/feedbackcategorysubject',feebacks_views.FeedbackCategorySubjectViewSet)
router.register(r'api/contactus',feebacks_views.ContactusViewSet)
urlpatterns = router.urls