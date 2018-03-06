Rails.application.routes.draw do
  get 'welcome/index'
 
  resources :documents do
  	resources :comments
  end
 
  root 'welcome#index'
end
