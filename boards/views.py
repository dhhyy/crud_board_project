# tag.name 이름으로 나오게 처리 good
# sqlite 이쁘게 나오게 하는 방법 강구
# 에러메세지 더 추가
# 테스트코드 하면서 하기
# 유닛테스트도 계속 하면서 진행
# readme 신경쓰기

# postman API 명세서 안됨

import json
import bcrypt

from django.views        import View
from django.http         import HttpResponse, JsonResponse
from boards.models       import Board, Tag
from users.utils         import LoginDecorator
from users.views         import User
# from django.db.models    import F, Count, Case, When

class PostingView(View):
    @LoginDecorator
    def post(self, request):
        
        try:
            data    = json.loads(request.body)
            title   = data['title']
            content = data['content']
            writer  = request.user
            tag     = Tag.objects.get(id=data['tag'])
            
            if not title or not content:
                return JsonResponse({'message' : 'CHECK_YOUR_INPUT'}, status=400)
            
            if Board.objects.filter(title=title).exists():
                return JsonResponse({'message' : 'SAME_TITLE, CHANGE TITLE'}, status=400)
            
            board = Board(
                title     = title,
                content   = content,
                writer    = writer,
                password  = request.user.password,
                tag       = tag
            )
            
            board.save()

            return JsonResponse({'message' : 'SUCCESS'}, status=200)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
class PostingDetailView(View):
    def get(self, request, board_id=None):
        try:
            boards = Board.objects.filter(id=board_id)

            for board in boards:
                board.hits += 1
                board.save()
            
            data = [
                {
                    'id'      : board.id,
                    'title'   : board.title,
                    'content' : board.content,
                    'hits'    : board.hits,
                    'writer'  : board.writer.name,
                    'tag'     : board.tag.name
                    } for board in boards]
            
            return JsonResponse({'message' : data}, status=200)

        except Board.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_BOARD_ID'}, status=400)
        
# class RePostingView(View):
#     @LoginDecorator
#     def post(self, request, board_id):
        
#         try:
#             data     = json.loads(request.body)
#             title    = data['title']
#             content  = data['content']
#             password = data['password']
#             board    = Board.objects.get(id=board_id)

#             if not bcrypt.checkpw(password.encode('UTF-8'), board.password.encode('UTF-8')):
#                 return JsonResponse({'message' : 'NOT_MATCHED_PASSWORD'}, status=401)
        
#             board.title    = title
#             board.content  = content

#             board.save()
            
#             return JsonResponse({'message' : 'SUCCESS'})
        
#         except KeyError:
#             return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

# class PostingDeleteView(View):
#     @LoginDecorator
#     def post(self, request, board_id):
        
#         try:
#             data     = json.loads(request.body)
#             password = data['password']
#             board    = Board.objects.get(id=board_id)
            
#             if not bcrypt.checkpw(password.encode('UTF-8'), board.password.encode('UTF-8')):
#                 return JsonResponse({'message' : 'NOT_MATCHED_PASSWORD'}, status=401)
                
#             board.delete()
        
#             return JsonResponse({'message' : 'SUCCESS'}, status=200)
        
#         except KeyError:
#             return JsonResponse({'message' : 'KEY_ERROR'})
        
# class PostingListView(View):
#     def get(self, request):
        
#         limit           = int(request.GET.get('limit', 0))
#         offset          = int(request.GET.get('offset', 0))
#         order_condition = request.GET.get('order',None) 
        
#         post_type_ordering = Case(
#             When(
#                 tag_id=1, then=1),
#                 default=0
#             )
        
#         boards = Board.objects.all().annotate(ordering=post_type_ordering).order_by('groupno', 'orderno')
        
#         if order_condition == "hits":
#             boards = Board.objects.order_by("hits")
            
#         if order_condition == "recents":
#             boards = Board.objects.order_by("create_at")
        
#         post_list = [
#             {
#                 'id'        : board.id,
#                 'title'     : board.title,
#                 'content'   : board.content,             
#                 'hits'      : board.hits,
#                 'groupno'   : board.groupno,
#                 'orderno'   : board.orderno,
#                 'depth'     : board.depth,
#                 'writer'    : board.writer.name,
#                 'tag'       : board.tag.name,
#                 'create_at' : board.create_at.strftime('%Y-%m-%d %H:%M:%S')
#                 } for board in boards][offset:limit]
                
#         return JsonResponse({'message' : post_list}, status=200)

# class ReplyPostingView(View):
#     @LoginDecorator
#     def post(self, request, board_id):
        
#         try:
#             data     = json.loads(request.body)
            
#             title    = data['title']
#             content  = data['content']
#             writer   = request.user
            
#             mother_board = Board.objects.get(id=board_id)
            
#             reply_list = Board.objects.filter(groupno = mother_board.groupno,
#                                             orderno__gt = mother_board.orderno)
        
#             child_board = Board(
#                 title    = title,
#                 content  = content,
#                 writer   = writer,
#                 password = request.user.password,
#                 tag      = Tag.objects.get(id=1)
#             )
            
#             child_board.save()
            
#             if reply_list:
#                 reply_list.update(orderno=F('orderno') + 1)
            
#             child_board.groupno = mother_board.groupno
#             child_board.orderno = mother_board.orderno+1
#             child_board.depth   = mother_board.depth+1
            
#             child_board.save()

#             return JsonResponse({'message' : 'SUCCESS'}, status=200)
        
#         except KeyError:
#             return JsonResponse({'message' : 'KEY_ERROR'}, status=400)