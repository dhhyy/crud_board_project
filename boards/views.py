import json
import bcrypt

from django.views        import View
from django.http         import HttpResponse, JsonResponse
from boards.models       import Board, Tag
from users.utils         import LoginDecorator
from users.views         import User

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
            board = Board.objects.get(id=board_id)
            
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
                    }
                ]

            return JsonResponse({'message' : data}, status=200)

        except Board.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_BOARD_ID'}, status=400)
        
class PostingListView(View):
    def get(self, request):
        
        try:
            limit           = int(request.GET.get('limit', 0))
            offset          = int(request.GET.get('offset', 0))
            order_condition = request.GET.get('order',None) 
        
            boards = Board.objects.all()

            if order_condition == "hits":
                boards = Board.objects.order_by("-hits")
            
            if order_condition == "recents":
                boards = Board.objects.order_by("create_at")
        
            board_list = [
                {
                    'id'        : board.id,
                    'title'     : board.title,
                    'content'   : board.content,             
                    'hits'      : board.hits,
                    'writer'    : board.writer.name,
                    'tag'       : board.tag.name,
                    'create_at' : board.create_at.strftime('%Y-%m-%d %H:%M:%S')
                    } for board in boards][offset:limit]
                
            return JsonResponse({'message' : board_list}, status=200)
        
        except ValueError:
            return JsonResponse({'message' : "ENTER page_number"}, status=400)
        
class RePostingView(View):
    @LoginDecorator
    def post(self, request, board_id):
        
        try:
            data     = json.loads(request.body)
            title    = data['title']
            content  = data['content']
            password = data['password']
            tag      = Tag.objects.get(id=data['tag'])
            board    = Board.objects.get(id=board_id)
            
            if not bcrypt.checkpw(password.encode('UTF-8'), board.password.encode('UTF-8')):
                return JsonResponse({'message' : 'NOT_MATCHED_PASSWORD'}, status=401)
        
            board.title    = title
            board.content  = content
            board.tag      = tag

            board.save()
            
            return JsonResponse({'message' : 'SUCCESS'})
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class PostingDeleteView(View):
    @LoginDecorator
    def post(self, request, board_id):
        
        try:
            data     = json.loads(request.body)
            password = data['password']
            
            board    = Board.objects.get(id=board_id)
            
            if not bcrypt.checkpw(password.encode('UTF-8'), board.password.encode('UTF-8')):
                return JsonResponse({'message' : 'NOT_MATCHED_PASSWORD'}, status=401)
                
            board.delete()
        
            return JsonResponse({'message' : 'SUCCESS'}, status=200)
        
        except Board.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_BOARD_ID'}, status=400)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)