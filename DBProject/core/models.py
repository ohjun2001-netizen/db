from django.db import models
from user.models import User  # user 앱의 User 모델 임포트
# courses 앱에서 참조할 모델 임포트
from courses.models import Class, ClassComment


# 캘린더 이벤트
class CalendarEvent(models.Model):
    event_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자")
    class_obj = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="강의")
    title = models.CharField(max_length=100, verbose_name="제목")
    description = models.TextField(verbose_name="설명")
    start_time = models.DateTimeField(verbose_name="시작 시간")
    end_time = models.DateTimeField(verbose_name="종료 시간")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 일시")

    class Meta:
        db_table = 'calendar_event'
        verbose_name = '캘린더 이벤트'
        verbose_name_plural = '캘린더 이벤트 목록'

    def __str__(self):
        return self.title


# 메신저 채널
class MessengerChannel(models.Model):
    channel_id = models.AutoField(primary_key=True)
    channel_name = models.CharField(max_length=100, verbose_name="채널명")
    channel_type = models.CharField(max_length=20, verbose_name="채널 유형")  # 상담, 조율 등 태그
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")

    class Meta:
        db_table = 'messenger_channel'
        verbose_name = '메신저 채널'
        verbose_name_plural = '메신저 채널 목록'

    def __str__(self):
        return self.channel_name


# 채널 참여자
class ChannelMember(models.Model):
    channel = models.ForeignKey(MessengerChannel, on_delete=models.CASCADE, verbose_name="채널")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자")

    class Meta:
        db_table = 'channel_member'
        verbose_name = '채널 멤버'
        verbose_name_plural = '채널 멤버 목록'
        unique_together = ('channel', 'user')  # 복합 기본 키 역할

    def __str__(self):
        return f"{self.channel.channel_name} - {self.user.name}"


# 메신저 메시지
class MessengerMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    channel = models.ForeignKey(MessengerChannel, on_delete=models.CASCADE, verbose_name="채널")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="보낸 사람")
    content = models.TextField(verbose_name="내용")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="전송 일시")
    is_read = models.BooleanField(default=False, verbose_name="읽음 여부")

    class Meta:
        db_table = 'messenger_messages'
        verbose_name = '메신저 메시지'
        verbose_name_plural = '메신저 메시지 목록'

    def __str__(self):
        return f"{self.sender.name}: {self.content[:20]}..."


# 강의 신청 및 수정 요청
class RequestClass(models.Model):
    request_id = models.AutoField(primary_key=True)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="요청 대상 강의")
    requester = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="요청자")
    request_type = models.CharField(max_length=10, verbose_name="요청 유형")
    requested_start_time = models.DateTimeField(verbose_name="요청 시작 시간")
    requested_end_time = models.DateTimeField(verbose_name="요청 종료 시간")

    APPROVAL_CHOICES = (
        ('승인', '승인'),
        ('거절', '거절'),
        ('보류', '보류'),
    )
    approved = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='보류', verbose_name="승인 상태")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='managed_requests', limit_choices_to={'role': 'manager'},
                                verbose_name="승인 매니저")
    is_read = models.BooleanField(default=False, verbose_name="수신 확인")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")

    class Meta:
        db_table = 'request_class'
        verbose_name = '강의 신청/수정 요청'
        verbose_name_plural = '강의 신청/수정 요청 목록'

    def __str__(self):
        return f"[{self.request_type}] {self.class_obj.class_name} 요청 - {self.approved}"


# 상담 요청
class MeetingRequest(models.Model):
    meeting_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_meetings',
                                limit_choices_to={'role': 'student'}, verbose_name="학생")
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_meetings',
                                   limit_choices_to={'role': 'instructor'}, verbose_name="강사")
    meeting_time = models.DateTimeField(verbose_name="상담 요청 시간")
    channel = models.ForeignKey('MessengerChannel', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name="일정 조율 채널")
    message = models.TextField(verbose_name="메시지 내용")
    is_read = models.BooleanField(default=False, verbose_name="읽음 여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")

    class Meta:
        db_table = 'meeting_request'
        verbose_name = '상담 요청'
        verbose_name_plural = '상담 요청 목록'

    def __str__(self):
        return f"{self.student.name}의 상담 요청 ({self.meeting_time.strftime('%Y-%m-%d %H:%M')})"


# 커뮤니티 게시판
class CommunityBoard(models.Model):
    board_id = models.AutoField(primary_key=True)
    board_title = models.CharField(max_length=100, verbose_name="게시판 제목")
    board_type = models.CharField(max_length=20, verbose_name="게시판 유형")

    class Meta:
        db_table = 'community_board'
        verbose_name = '커뮤니티 게시판'
        verbose_name_plural = '커뮤니티 게시판 목록'

    def __str__(self):
        return self.board_title


# 커뮤니티 게시글
class CommunityPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    board = models.ForeignKey(CommunityBoard, on_delete=models.CASCADE, verbose_name="게시판")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    post_title = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 일시")
    open = models.BooleanField(default=True, verbose_name="공개 여부")
    view = models.IntegerField(default=0, verbose_name="조회수")

    class Meta:
        db_table = 'community_post'
        verbose_name = '커뮤니티 게시글'
        verbose_name_plural = '커뮤니티 게시글 목록'

    def __str__(self):
        return self.post_title


# 커뮤니티 댓글
class CommunityComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, verbose_name="게시글")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    comment_content = models.TextField(verbose_name="댓글 내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")

    class Meta:
        db_table = 'community_comment'
        verbose_name = '커뮤니티 댓글'
        verbose_name_plural = '커뮤니티 댓글 목록'

    def __str__(self):
        return f"{self.author.name}의 댓글 ({self.post.post_title})"


# 알림
class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="수신 사용자")
    notification_type = models.CharField(max_length=30, verbose_name="알림 유형")
    message = models.TextField(verbose_name="메시지")

    # 참조할 알림 사항들
    class_request = models.ForeignKey(RequestClass, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name="강의 요청 참조")
    meeting = models.ForeignKey(MeetingRequest, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name="상담 요청 참조")
    event = models.ForeignKey(CalendarEvent, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="이벤트 참조")
    class_comment = models.ForeignKey(ClassComment, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name="강의 댓글 참조")
    community_comment = models.ForeignKey(CommunityComment, on_delete=models.SET_NULL, null=True, blank=True,
                                          verbose_name="커뮤니티 댓글 참조")

    is_read = models.BooleanField(default=False, verbose_name="읽음 여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")

    class Meta:
        db_table = 'notification'
        verbose_name = '알림'
        verbose_name_plural = '알림 목록'

    def __str__(self):
        return f"[{self.notification_type}] {self.message[:30]}..."