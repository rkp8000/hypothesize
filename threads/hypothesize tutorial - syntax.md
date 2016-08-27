This thread demonstrates how to generate hyperlinks and styled elements. Click on the "edit" button above to see the syntax used for each special element.

### *hypothesize* syntax:

Basic link to thread: ((start here!)).

Link to thread with custom link text: ((start here!|link to the tutorial)).

Link to document: [[Hypothesize2016]].

Link to document with custom link text: [[Hypothesize2016|software license]].

### Markdown syntax:

**bold**

*italics*

Unordered list:

* bullet point
* bullet point
* bullet point with nested unordered list
    * nested bullet point
    * nested bullet point
* bullet point

Ordered list

1. Thing 1
2. Thing 2
    1. Thing 1 nested in Thing 2
    2. Thing 2 nested in Thing 2
3. Thing 3

# Header 1
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6

Link to external webpage with custom link text: [a fancier Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).

Embedded external image:

![hypothesize logo](https://raw.githubusercontent.com/rkp8000/hypothesize/master/logo_small.png "hypothesize logo")

Embedded external gif:

![alt text](https://upload.wikimedia.org/wikipedia/commons/1/16/Parallax-scroll-example.gif)

TeX equations (note that in this version of *hypothesize* equations only render correctly if their container thread is opened as a new page):

* inline style: $x^2 + y^2 = z^2$
* block style:

$$r = \sum \limits_i \cfrac{1}{a_i^z}$$

Code:

```x = 5; y = 6```