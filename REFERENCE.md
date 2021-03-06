# HamlPy Reference

# Table of Contents

- [Plain Text](#plain-text)
- [Doctype](#doctype)
- [HTML Elements](#html-elements)
    - [Element Name: %](#element-name-)
    - [Attributes: {} or ()](#attributes-)
        - [Attributes without values (Boolean attributes)](#attributes-without-values-boolean-attributes)
        - ['class' and 'id' attributes](#class-and-id-attributes)
    - [Class and ID: . and #](#class-and-id--and-)
        - [Implicit div elements](#implicit-div-elements)
    - [Self-Closing Tags: /](#self-closing-tags-)
- [Comments](#comments)
    - [HTML Comments /](#html-comments-)
    - [Conditional Comments /[]](#conditional-comments-)
    - [HamlPy Comments: -#](#hamlpy-comments--)
- [Django Specific Elements](#django-specific-elements)
    - [Django Variables: =](#django-variables-)
    - [Inline Django Variables: ={...}](#inline-django-variables-)
    - [Django Tags: -](#django-tags--)
        - [Tags within attributes:](#tags-within-attributes)
    - [Whitespace removal](#whitespace-removal)
- [Filters](#filters)
    - [:plain](#plain)
    - [:javascript](#javascript)
    - [:coffeescript or :coffee](#coffeescript-or-coffee)
    - [:cdata](#cdata)
    - [:css](#css)
    - [:stylus](#stylus)
    - [:markdown](#markdown)
    - [:highlight](#highlight)
    - [:python](#python)

## Plain Text

Any line that is not interpreted as something else will be taken as plain text and outputted unmodified.  For example:

```haml
%gee
    %whiz
        Wow this is cool!
```

is compiled to:

```htmldjango
<gee>
    <whiz>
        Wow this is cool!
    </whiz>
</gee>
```

## Doctype

You can specify a specific doctype after the !!! The following doctypes are supported:

* `!!!`: XHTML 1.0 Transitional
* `!!! Strict`: XHTML 1.0 Strict
* `!!! Frameset`: XHTML 1.0 Frameset
* `!!! 5`: XHTML 5
* `!!! 1.1`: XHTML 1.1
* `!!! XML`: XML prolog

## HTML Elements

### Element Name: %

The percent character placed at the beginning of the line will then be followed by the name of the element, then optionally modifiers (see below), a space, and text to be rendered inside the element.  It creates an element in the form of <element></element>.  For example:

```haml
%one
    %two
        %three Hey there
```

is compiled to:

```htmldjango
<one>
    <two>
        <three>Hey there</three>
    </two>
</one>
```

Any string is a valid element name and an opening and closing tag will automatically be generated.

### Attributes: {} or ()

Haml has three different styles for attributes which are all supported. For example:

```haml
%html{:xmlns => 'http://www.w3.org/1999/xhtml', :lang => 'en'}

%html{'xmlns': 'http://www.w3.org/1999/xhtml', 'lang': 'en'}

%html(xmlns='http://www.w3.org/1999/xhtml' lang='en')
```

are all compiled to:

```htmldjango
<html xmlns='http://www.w3.org/1999/xhtml' lang='en'></html>
```

Long attribute dictionaries can be separated into multiple lines:

```haml
%script(type='text/javascript' charset='utf-8'
        href='/long/url/to/javascript/resource.js')
```

#### Attributes without values (Boolean attributes)

Attributes without values can be specified using singe variable. For example:

```haml
%input(type='checkbox' value='Test' checked)
```

is compiled to:

```htmldjango
<input type="checkbox" value="Test" checked />
```

Alternatively the values can be specified using Python's ```None``` keyword (without quotes). For example:

```haml
%input(type='checkbox' value='Test' checked=None)
```

is compiled to:

```htmldjango
<input type="checkbox" value="Test" checked />
```


#### 'class' and 'id' attributes

The 'class' and 'id' attributes can also be specified as a Python tuple whose elements will be joined together.  A 'class' tuple will be joined with " " and an 'id' tuple is joined with "_".  For example:

```haml
%div{'id': ('article', '3'), 'class': ('newest', 'urgent')} Content
```

is compiled to:

```htmldjango
<div id='article_3' class='newest urgent'>Content</div>
```

### Class and ID: . and #

The period and pound sign are borrowed from CSS.  They are used as shortcuts to specify the class and id attributes of an element, respectively.  Multiple class names can be specified by chaining class names together with periods.  They are placed immediately after a tag and before an attribute dictionary.  For example:

```haml
%div#things
    %span#rice Chicken Fried
    %p.beans{'food':'true'} The magical fruit
    %h1#id.class.otherclass La La La
```

is compiled to:

```htmldjango
<div id='things'>
    <span id='rice'>Chiken Fried</span>
    <p class='beans' food='true'>The magical fruit</p>
    <h1 id='id' class='class otherclass'>La La La</h1>
</div>
```

And,

```haml
%div#content
    %div.articles
        %div.article.title Doogie Howser Comes Out
        %div.article.date 2006-11-05
        %div.article.entry
            Neil Patrick Harris would like to dispel any rumors that he is straight

is compiled to:
```

```htmldjango
<div id='content'>
    <div class='articles'>
        <div class='article title'>Doogie Howser Comes Out</div>
        <div class='article date'>2006-11-05</div>
        <div class='article entry'>
            Neil Patrick Harris would like to dispel any rumors that he is straight
        </div>
    </div>
</div>
```

These shortcuts can be combined with the attribute dictionary and they will be combined as if they were all put inside a list.  For example:

```haml
%div#Article.article.entry{'id':'1', 'class':'visible'} Booyaka
```

is equivalent to:

```haml
%div{'id':['Article','1'], 'class':['article','entry','visible']} Booyaka
```

and would compile to:

```htmldjango
<div id='Article_1' class='article entry visible'>Booyaka</div>
```

#### Implicit div elements

Because divs are used so often, they are the default element.  If you only define a class and/or id using `.` or `#` then the %div will be implied.  For example:

```haml
#collection
    .item
        .description What a cool item!
```

will compile to:

```htmldjango
<div id='collection'>
    <div class='item'>
        <div class='description'>What a cool item!</div>
    </div>
</div>
```

### Self-Closing Tags: /

The forward slash character, when placed at the end of a tag definition, causes the tag to be self-closed.  For example:

```haml
%br/
%meta{'http-equiv':'Content-Type', 'content':'text/html'}/
```

will compile to:

```htmldjango
<br />
<meta http-quiv='Content-Type' content='text/html' />
```

Some tags are automatically closed, as long as they have no content.  `meta, img, link, script, br` and `hr` tags are automatically closed.  For example:

```haml
%br
%meta{'http-equiv':'Content-Type', 'content':'text/html'}
```

will compile to:

```htmldjango
<br />
<meta http-quiv='Content-Type' content='text/html' />
```

## Comments

There are two types of comments supported:  those that show up in the HTML and those that don't.

### HTML Comments /

The forward slash character, when placed at the beginning of a line, wraps all the text after it in an HTML comment.  For example:

```haml
%peanutbutterjelly
    / This is the peanutbutterjelly element
    I like sandwiches!
```

is compiled to:

```htmldjango
<peanutbutterjelly>
    <!-- This is the peanutbutterjelly element -->
    I like sandwiches!
</peanutbutterjelly>
```

The forward slash can also wrap indented sections of code.  For example:

```haml
/
    %p This doesn't render
    %div
        %h1 Because it's commented out!
```

is compiled to:

```htmldjango
<!--
    <p>This doesn't render</p>
    <div>
        <h1>Because it's commented out!</h1>
    </div>
-->
```

### Conditional Comments /[]

You can use [Internet Explorer conditional comments](http://www.quirksmode.org/css/condcom.html) by enclosing the condition in square brackets after the /. For example:

```haml
/[if IE]
    %h1 Get a better browser
```

is compiled to:

```htmldjango
<!--[if IE]>
    <h1>Get a better browser</h1>
<![endif]-->
```

### HamlPy Comments: -#

The hyphen followed immediately by the pound sign signifies a silent comment.  Any text following this isn't rendered during compilation at all.  For example:

```haml
%p foo
-# Some comment
%p bar
```

is compiled to:

```htmldjango
<p>foo</p>
<p>bar</p>
```

## Django Specific Elements

The key difference in HamlPy from Haml is the support for Django elements.  The syntax for ruby evaluation is borrowed from Haml and instead outputs Django tags and variables.

### Django Variables: =

A line starting with an equal sign followed by a space and then content is evaluated as a Django variable.  For example:

```haml
.article
    .preview
        = story.teaser
```

is compiled to:

```htmldjango
<div class='article'>
    <div class='preview'>
        {{ story.teaser }}
    </div>
</div>
```

A Django variable can also be used as content for any HTML element by placing an equals sign as the last character before the space and content.  For example:

```haml
%h2
    %a{'href':'stories/1'}= story.teaser
```

is compiled to:

```htmldjango
<h2>
    <a href='stories/1'>{{ story.teaser }}</a>
</h2>
```

### Inline Django Variables: #{...}

You can also use inline variables using the `#{...}` syntax. For example:

```haml
Hello #{name}, how are you today?
```

is compiled to

```htmldjango
Hello {{ name }}, how are you today?
```

Inline variables can also be used in an element's attribute values. For example:

```haml
%a{'title':'Hello #{name}, how are you?'} Hello
```

is compiled to:

```htmldjango
<a title='Hello {{ name }}, how are you?'>Hello</a>
```

Inline variables can be escaped by placing a `\` before them. For example:

```haml
Hello \#{name}
```

is compiled to:

```htmldjango
Hello #{name}
```

Django style `={...}` syntax is also optionally supported. If you are using the template loader
then ensure `HAMLPY_DJANGO_INLINE_STYLE` is `True`, and the two syntaxes can then be used interchangeably.



### Django Tags: -

The hypen character at the start of the line followed by a space and a Django tag will be inserted as a Django tag.  For example:

```haml
- block content
    %h1= section.title

    - for dog in dog_list
        %h2
            = dog.name
```

is compiled to:

```htmldjango
{% block content %}
    <h1>{{ section.title }}</h1>

    {% for dog in dog_list %}
        <h2>
            {{ dog.name }}
        </h2>
    {% endfor %}
{% endblock %}
```


Notice that block, for, if and else, as well as ifequal, ifnotequal, ifchanged and 'with' are all automatically closed.  Using endfor, endif, endifequal, endifnotequal, endifchanged or endblock will throw an exception.

#### Tags within attributes:

This is not yet supported: `%div{'attr':"- firstof var1 var2 var3"}` will not insert the `{% ... %}`.

The workaround is to insert actual django template tag code into the haml. For example:

```haml
%a{'href': "{% url socialauth_begin 'github' %}"} Login with Github
```

is compiled to:

```htmldjango
<a href="{% url socialauth_begin 'github' %}">Login with Github</a>
```


### Whitespace removal

Sometimes we want to remove whitespace inside or around an element, usually to fix the spacing problem with inline-block elements (see "The Enormous Drawback" section of [this article](http://robertnyman.com/2010/02/24/css-display-inline-block-why-it-rocks-and-why-it-sucks/) for more details).

To remove leading and trailing spaces **inside** a node ("inner whitespace removal"), use the `<` character after an element. For example, this:

```haml
%div
    %pre<
        = Foo
```

is compiled to:

```htmldjango
<div>
  <pre>{{ Foo }}</pre>
</div>
```

To remove leading and trailing spaces **around** a node ("outer whitespace removal"), use the `>` character after an element. For example, this:

```haml
%li Item one
%li> Item two
%li Item three
```

is compiled to:

```htmldjango
<li>Item one</li><li>Item two</li><li>Item three</li>
```

## Filters

### :plain

Does not parse the filtered text. This is useful for large blocks of text without HTML tags, when you don’t want lines starting with . or - to be parsed.

### :javascript

Surrounds the filtered text with &lt;script type="text/javascript"&gt; and CDATA tags. Useful for including inline Javascript.

### :coffeescript or :coffee

Surrounds the filtered text with &lt;script type="text/coffeescript"&gt; and CDATA tags. Useful for including inline Coffeescript.

### :cdata

Surrounds the filtered text with CDATA tags.

### :css

Surrounds the filtered text with &lt;style type="text/css"&gt; and CDATA tags. Useful for including inline CSS.

### :stylus

Surrounds the filtered text with &lt;style type="text/stylus"&gt; and CDATA tags. Useful for including inline Stylus.

### :markdown

Converts the filter text from Markdown to HTML, using the Python [Markdown library](http://freewisdom.org/projects/python-markdown/).

You can also specify the enabled extensions using the setting HAMLPY_MARKDOWN_EXTENSIONS and assigning a list of valid extensions to it. See [Markdown library extensions documentation](https://python-markdown.github.io/extensions/) for available extensions. For example:

```python
HAMLPY_MARKDOWN_EXTENSIONS = ['extras']
```

### :highlight

This will output the filtered text with syntax highlighting using [Pygments](http://pygments.org).

For syntax highlighting to work correctly, you will also need to generate or include a Pygments CSS file. See
the section ["Generating styles"](http://pygments.org/docs/cmdline/#generating-styles) in the Pygments
documentation for more information.

### :python

Execute the filtered text as python and output the result in the file. For example:

```haml
:python
    for i in range(0, 5):
        print "<p>item %s</p>" % i
```

is compiled to:

```htmldjango
<p>item 0</p>
<p>item 1</p>
<p>item 2</p>
<p>item 3</p>
<p>item 4</p>
```

