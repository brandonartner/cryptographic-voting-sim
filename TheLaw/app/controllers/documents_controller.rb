class DocumentsController < ApplicationController
	
	http_basic_authenticate_with name: 'brandon', password: 'secret', except: [:index,:show]

	def index
	    @documents = Document.all
	end

	def show
		@document = Document.find(params[:id])
	end

	def new
		@document = Document.new
	end

	def edit
		@document = Document.find(params[:id])
	end

	def create
		@document = Document.new(document_params)
	 
		if @document.save
	  		redirect_to @document
	  	else
	  		render 'new'
	  	end
	end

	def update
		@document = Document.find(params[:id])

		if @document.update(document_params)
			redirect_to @document
		else
			render 'new'
		end
	end

	def destroy
		@document = Document.find(params[:id])
		@document.destroy

		redirect_to documents_path
	end
	 
	private
		def document_params
			params.require(:document).permit(:title, :text)
		end
end
