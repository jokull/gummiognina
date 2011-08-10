if typeof window.console == "undefined" or typeof window.console.log == "undefined"
  window.console = log: ->

window.GummiNina.collections = {}
window.GummiNina.models = {}
window.GummiNina.views = {}


class window.Router extends Backbone.Router
  
  routes: 
    "/photo-:id": "page"
    
  page: (id) ->
    # TODO paginate until this id is found
    GummiNina.collections.photos.page()

class window.Photo extends Backbone.Model
  
class window.Photos extends Backbone.Collection
  
  model: Photo
  
  url: =>
    "/photos/page-" + GummiNina.max_tag_id
  
  parse: (response) =>
    response.photos
  
  page: =>
    Backbone.sync "read", @, success: (resp) =>
      GummiNina.max_tag_id = resp.max_tag_id
      @add (@parse resp)
      @trigger "more"
      # GummiNina.router.navigate @last_id()


class window.PhotoView extends Backbone.View
  
  className: "photo"
  
  initialize: (options) ->
    @model.bind "change", @render
    @model.view = @
    @render()
  
  last: =>
    ($ @el).appear (event) =>
      @model.collection.page()
    , one: true
  
  render: =>
    tpl = _.template($("#tpl-photo").html())
    ($ @el).html (tpl @model.toJSON())
    return @
  

class window.PhotosView extends Backbone.View
  
  el: "#photos"
  
  initialize: (options) ->
    @collection.bind "add", @add
    @collection.bind "reset", @reset
    @collection.bind "more", @more
  
  more: =>
    # if @model.collection.last() == @model
    @collection.last().view.last()
  
  reset: =>
    ($ ".photos-list", @el).html ""
    @collection.each @add
    @collection.last().view.last()
  
  add: (model) =>
    model.view = new window.PhotoView model: model
    (@$ ".photos-list").append model.view.render().el
    return model
  

$ ->

  GummiNina.router = new Router
  GummiNina.collections.photos = new Photos
  GummiNina.views.photos = new PhotosView
    collection: GummiNina.collections.photos
  GummiNina.collections.photos.reset window.GummiNina.photos
  
  Backbone.history.start()
