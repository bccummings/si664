from django.contrib import admin

# Register your models here.
from catalog.models import Author, Genre, Book, BookInstance, Language

# register Author (note, can also replace third line with @admin.register(Author) as decorator before class definition)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# register Book
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]
admin.site.register(Book, BookAdmin)

# register BookInstance
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status', 'due_back', 'id')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
admin.site.register(BookInstance, BookInstanceAdmin)

# these two are simple, so no need to go through class configuration
admin.site.register(Genre)
admin.site.register(Language)
