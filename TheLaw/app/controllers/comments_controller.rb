class CommentsController < ApplicationController
	
	http_basic_authenticate_with name: 'brandon', password: 'secret', only :destroy

	def create
		@document = Document.find(params[:document_id])
		@comment = @document.comments.create(comment_params)
		redirect_to document_path(@document)
	end

	#def show
	#	
	#end

	#def update
	#	
	#end

	def destroy
		@document = Document.find(params[:document_id])
		@comment = @document.comments.find(params[:id])
		@comment.destroy
		redirect_to document_path(@document)
	end

	private
		def comment_params
			params.require(:comment).permit(:commenter,:body)
		end
end
