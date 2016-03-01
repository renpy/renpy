# Markdown Issue Guide
Basic guide to ease issues solution by using *GitHub Flavored Markdown*.

## What is Markdown?
If you don't know what is Markdown, take a look at this [basic tutorial](https://guides.github.com/features/mastering-markdown/).

## Showing piece of code in your issue

Using Markdown [code block](https://help.github.com/articles/creating-and-highlighting-code-blocks/), set the language to Ren'Py typing `renpy` after the <code>```</code>:

<pre><code>
```renpy
# Ren'Py statements
```
</code></pre>

## Showing errors and trackbacks

Using code block again, set the language to `python-traceback`.

<pre><code>
```python-traceback
# Content of the "traceback.txt"
```
</code></pre>

***

## Simple issue example

A simple error caused by an undefined character:

```renpy
define test_char = Character('Test Char')

label start:

    centered "Centered text"
    test_char "Hello, world!"
    undefined_char "Hello!"
    
    return
```

Traceback file:

```python-traceback
I'm sorry, but an uncaught exception occurred.

While running game code:
  File "game/script.rpy", line 8, in script
    undefined_char "Hello!"
Exception: Sayer 'undefined_char' is not defined.

-- Full Traceback ------------------------------------------------------------

Full traceback:
  File "game/script.rpy", line 8, in script
    undefined_char "Hello!"
  File "C:\Users\tumeo\Documents\Renpy\renpy-6.99.7-sdk\renpy\ast.py", line 583, in execute
    who = eval_who(self.who, self.who_fast)
  File "C:\Users\tumeo\Documents\Renpy\renpy-6.99.7-sdk\renpy\ast.py", line 500, in eval_who
    raise Exception("Sayer '%s' is not defined." % who.encode("utf-8"))
Exception: Sayer 'undefined_char' is not defined.

Windows-8-6.2.9200
Ren'Py 6.99.7.858
simple_test 0.0
```
