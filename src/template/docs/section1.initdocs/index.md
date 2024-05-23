# InitDocs Components

On this page, you can find a plethora of blocks to use when writing your documentation. This template implements `mcdocs-material`, which also has a [reference page](https://squidfunk.github.io/mkdocs-material/reference/) of their own. The intention of this page, however, is to show all of the configured functionality that this template supports, with easily accessible code implementations to ease your writing.

## Block Components

### Anchors

#### Markdown links

[This is a regular markdown link](https://github.com/MartinJohannesNilsen/InitDocs)

??? example "Code"

        [This is a regular markdown link](https://github.com/MartinJohannesNilsen/InitDocs)

#### HTML Anchor links

##### Replace Current Path

<a href="https://github.com/MartinJohannesNilsen/InitDocs">This is a regular html anchor, which will be opened in the current tab</a>

??? example "Code"

        <a href="[link]">This is a regular html anchor, which will be opened in the current tab</a>

##### Open In New Tab

<a href="https://github.com/MartinJohannesNilsen/InitDocs" target="_blank">This is a link which will be opened in new tab</a>

??? example "Code"

        <a href="[link]" target="_blank">This is a link which will be opened in new tab</a>

##### Download Link

<a href="https://github.com/MartinJohannesNilsen/InitDocs/blob/main/readme.md" download>This is a download link</a>

??? example "Code"

        <a href="[link]" download>This is a download link</a>

### Annotations

#### In Text

Lorem ipsum dolor sit amet, (1) consectetur adipiscing elit.
{ .annotate }

1.  :man_raising_hand: I'm an annotation! I can contain `code`, __formatted
    text__, images, ... basically anything that can be expressed in Markdown.

??? example "Code"

        Lorem ipsum dolor sit amet, (1) consectetur adipiscing elit.
        { .annotate }

        1.  :man_raising_hand: I'm an annotation! I can contain `code`, __formatted
            text__, images, ... basically anything that can be expressed in Markdown.


#### Nested Annotations

Lorem ipsum dolor sit amet, (1) consectetur adipiscing elit.
{ .annotate }

1.  :man_raising_hand: I'm an annotation! (1)
    { .annotate }

    1.  :woman_raising_hand: I'm an annotation as well!
   
??? example "Code"

        Lorem ipsum dolor sit amet, (1) consectetur adipiscing elit.
        { .annotate }

        1.  :man_raising_hand: I'm an annotation! (1)
            { .annotate }

            1.  :woman_raising_hand: I'm an annotation as well!

#### In Callouts

!!! note annotate "Phasellus posuere in sem ut cursus (1)"

    Lorem ipsum dolor sit amet, (2) consectetur adipiscing elit. Nulla et
    euismod nulla. Curabitur feugiat, tortor non consequat finibus, justo
    purus auctor massa, nec semper lorem quam in massa.

1.  :man_raising_hand: I'm an annotation!
2.  :woman_raising_hand: I'm an annotation as well!
   
??? example "Code"

        !!! note annotate "Phasellus posuere in sem ut cursus (1)"

            Lorem ipsum dolor sit amet, (2) consectetur adipiscing elit. Nulla et
            euismod nulla. Curabitur feugiat, tortor non consequat finibus, justo
            purus auctor massa, nec semper lorem quam in massa.

        1.  :man_raising_hand: I'm an annotation!
        2.  :woman_raising_hand: I'm an annotation as well!

#### In Content Tabs

=== "Tab 1"

    Lorem ipsum dolor sit amet, (1) consectetur adipiscing elit.
    { .annotate }

    1.  :man_raising_hand: I'm an annotation!

=== "Tab 2"

    Phasellus posuere in sem ut cursus (1)
    { .annotate }

    1.  :woman_raising_hand: I'm an annotation as well!
   
??? example "Code"

        === "Tab 1"

            Lorem ipsum dolor sit amet, (1) consectetur adipiscing elit.
            { .annotate }

            1.  :man_raising_hand: I'm an annotation!

        === "Tab 2"

            Phasellus posuere in sem ut cursus (1)
            { .annotate }

            1.  :woman_raising_hand: I'm an annotation as well!


#### In Code Blocks

##### Default Format

Code annotations can be placed anywhere in a code block where a comment for the language of the block can be placed, e.g. for JavaScript in `// ...` and `/* ... */`, for YAML in `# ...`, etc.

``` yaml
theme:
  features:
    - content.code.annotate # (1)
```

1.  :man_raising_hand: I'm a code annotation! I can contain `code`, __formatted
    text__, images, ... basically anything that can be written in Markdown.

??? example "Code"

        ``` yaml
        theme:
        features:
            - content.code.annotate # (1)
        ```

        1.  :man_raising_hand: I'm a code annotation! I can contain `code`, __formatted
            text__, images, ... basically anything that can be written in Markdown.

##### Stripping Comments

If you wish to strip the comment characters surrounding a code annotation, simply add an `!` after the closing parenthesis of the code annotation:

``` yaml
# (1)!
```

1.  Look ma, less line noise!
   
??? example "Code"

        ``` yaml
        # (1)!
        ```

        1.  Look ma, less line noise!

#### In Everything Else

We can add annotations to most elements using the attribute list approach, but there are some limitations. However, it's always possible (except for tables as of now) to leverage markdown in HTML, where we can wrap elements with a `<div>` tag and the `annotate` class:

<div class="annotate" markdown>

> Lorem ipsum dolor sit amet, (1) consectetur adipiscing elit.

</div>

1.  :man_raising_hand: I'm an annotation!

??? example "Code"

        <div class="annotate" markdown>

        > Lorem ipsum dolor sit amet, (1) consectetur adipiscing elit.

        </div>

        1.  :man_raising_hand: I'm an annotation!

With this trick, we can add annotatins to blockquotes, lists, and many other elements that are not supported by the attribute lists extenion. 

### Buttons

#### Outlined

[Subscribe to our newsletter](#){ .md-button }

??? example "Code"

        [Subscribe to our newsletter](#){ .md-button }

#### Primary

[Subscribe to our newsletter](#){ .md-button .md-button--primary }

??? example "Code"

        [Subscribe to our newsletter](#){ .md-button .md-button--primary }

#### Icon Button

[Send :fontawesome-solid-paper-plane:](#){ .md-button }

??? example "Code"

        [Send :fontawesome-solid-paper-plane:](#){ .md-button }


### Callouts

Callouts, or "admonitions", can be made with just a few `!!!` or ``???`. Read the next subsections for how to make different types of callouts.

#### Types

??? note

    ```
    !!! note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    ```

??? abstract

    ```
    !!! abstract

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    ```

??? info

    ```
    !!! info

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    ```

??? tip

    ```
    !!! tip

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    ```

??? success

    ```
    !!! success

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    ```

??? question

    ```
    !!! question

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    ```

??? warning

    ```
    !!! warning

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    ```

??? failure

    ```
    !!! failure

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    ```

??? danger

    ```
    !!! danger

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    ```

??? bug

    ```
    !!! bug

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    ```

??? example

    ```
    !!! example

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    ```

??? quote

    ```
    !!! quote

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    ```



#### Default Format

##### With Standard Title (Type)

!!! note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

??? example "Code"
    
    ```
    !!! note

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
        nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
        massa, nec semper lorem quam in massa.
    ```

##### Defined Title

!!! note "Title"

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

??? example "Code"

    ```
    !!! note "Title"

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
        nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
        massa, nec semper lorem quam in massa.
    ```

##### No Title Row

!!! note ""

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

??? example "Code"

    ```
    !!! note ""

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
        nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
        massa, nec semper lorem quam in massa.
    ```

#### Collapsibles

##### Expanded By Default

???+ note 

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

??? example "Code"

    ```
    ???+ note 

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
        nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
        massa, nec semper lorem quam in massa.
    ```

##### Closed By Default

??? note 

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

??? example "Code"

    ```
    ??? note 

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
        nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
        massa, nec semper lorem quam in massa.
    ```

#### Inline

=== "Left"

    !!! info inline "Inline left"

        This is inline left

    ```
    !!! info inline "Inline left"

        This is inline left
    ```

=== "Right"

    !!! tip inline end "Inline right"

        This is inline right

    ```
    !!! tip inline end "Inline right"

        This is inline right
    ```

### Code

#### Add a Title

``` py title="bubble_sort.py"
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```

??? example "Code"

        ``` py title="bubble_sort.py"
        def bubble_sort(items):
            for i in range(len(items)):
                for j in range(len(items) - 1 - i):
                    if items[j] > items[j + 1]:
                        items[j], items[j + 1] = items[j + 1], items[j]
        ```

#### Line Numbers

``` py linenums="1"
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```

??? example "Code"

        ``` py linenums="1"
        def bubble_sort(items):
            for i in range(len(items)):
                for j in range(len(items) - 1 - i):
                    if items[j] > items[j + 1]:
                        items[j], items[j + 1] = items[j + 1], items[j]
        ```

#### Syntax Hightlighting

**Block**

```py
print("hello world")
```

??? example "Code"
    
        ```py
        print("hello world")
        ```

**Inline**     
    
The `#!python range()` function is used to generate a sequence of numbers. Here, we used `#!` followed by a [language shortcode](https://pygments.org/docs/lexers/). After space, we can write our inline code.

??? example "Code"
    
        The `#!python range()` function is used to generate a sequence of numbers. Here, we used `#!` followed by a [language shortcode](https://pygments.org/docs/lexers/). After space, we can write our inline code.



#### Line hightlighting

We can hightlight specific lines, or segments of lines.

```hl_lines="2 4-5"
I am not hightlighted
I am hightlighted

We are hightlighted
Yes we are
```

??? example "Code"

        ```hl_lines="2 4-5"
        I am not hightlighted
        I am hightlighted

        We are hightlighted
        Yes we are
        ```


### Comment Out Sections

For commenting out a section, you may use regular HTML comments. That is, encapsulate the text in `<!--` and `-->`.

<!--
THIS IS COMMENTED OUT
-->

??? example "Code"

    ```hl_lines="1 3"
    <!--
    THIS IS COMMENTED OUT
    -->     
    ```

### Content Tabs

#### General Format

=== "Unordered list"

    * Sed sagittis eleifend rutrum
    * Donec vitae suscipit est
    * Nulla tempor lobortis orci

=== "Ordered list"

    1. Sed sagittis eleifend rutrum
    2. Donec vitae suscipit est
    3. Nulla tempor lobortis orci

??? example "Code"

    ```
    === "Unordered list"

        * Sed sagittis eleifend rutrum
        * Donec vitae suscipit est
        * Nulla tempor lobortis orci

    === "Ordered list"

        1. Sed sagittis eleifend rutrum
        2. Donec vitae suscipit est
        3. Nulla tempor lobortis orci
    ```


#### Code Blocks

=== "C"

    ``` c
    #include <stdio.h>

    int main(void) {
      printf("Hello world!\n");
      return 0;
    }
    ```

=== "C++"

    ``` c++
    #include <iostream>

    int main(void) {
      std::cout << "Hello world!" << std::endl;
      return 0;
    }
    ```

??? example "Code"

    ```
    === "C"

        ``` c
        #include <stdio.h>

        int main(void) {
        printf("Hello world!\n");
        return 0;
        }
        ```

    === "C++"

        ``` c++
        #include <iostream>

        int main(void) {
        std::cout << "Hello world!" << std::endl;
        return 0;
        }
        ```
    ```


#### Embedded Content

Can also be embedded in other components, such as admonitions (callouts)

!!! example

    === "Unordered List"

        ``` markdown
        * Sed sagittis eleifend rutrum
        * Donec vitae suscipit est
        * Nulla tempor lobortis orci
        ```

    === "Ordered List"

        ``` markdown
        1. Sed sagittis eleifend rutrum
        2. Donec vitae suscipit est
        3. Nulla tempor lobortis orci
        ```

??? example "Code"

    ```
    !!! example

        === "Unordered List"

            ``` markdown
            * Sed sagittis eleifend rutrum
            * Donec vitae suscipit est
            * Nulla tempor lobortis orci
            ```

        === "Ordered List"

            ``` markdown
            1. Sed sagittis eleifend rutrum
            2. Donec vitae suscipit est
            3. Nulla tempor lobortis orci
            ```
    ```

### Diagrams

This project support diagrams through Kroki. To see a full list of reference diagrams, refer to the [Kroki example page](https://kroki.io/examples.html). You might also want to [read more](https://pypi.org/project/mkdocs-kroki-plugin/) about the plugin we have used as well.

For rendering diagrams, simply use code fences (code block syntax) with a tag in the format `kroki-<module>`. To find the correct module, refer to the diagram type subtitles on the [example page](https://kroki.io/examples.html), and remember to write it in lowercase. You can also add optional [diagram options](https://docs.kroki.io/kroki/setup/diagram-options/).

#### Block Diagrams

`kroki-blockdiag`:

```kroki-blockdiag no-transparency=false
blockdiag {
  blockdiag -> generates -> "block-diagrams";
  blockdiag -> is -> "very easy!";

  blockdiag [color = "greenyellow"];
  "block-diagrams" [color = "pink"];
  "very easy!" [color = "orange"];
}
```

??? example "Code"

        blockdiag {
          blockdiag -> generates -> "block-diagrams";
          blockdiag -> is -> "very easy!";

          blockdiag [color = "greenyellow"];
          "block-diagrams" [color = "pink"];
          "very easy!" [color = "orange"];
        }


#### Network Diagrams

`kroki-nwdiag`:

```kroki-nwdiag
nwdiag {
  network dmz {
    address = "210.x.x.x/24"

    web01 [address = "210.x.x.1"];
    web02 [address = "210.x.x.2"];
  }
  network internal {
    address = "172.x.x.x/24";

    web01 [address = "172.x.x.1"];
    web02 [address = "172.x.x.2"];
    db01;
    db02;
  }
}
```

??? example "Code"

        nwdiag {
          network dmz {
            address = "210.x.x.x/24"

            web01 [address = "210.x.x.1"];
            web02 [address = "210.x.x.2"];
          }
          network internal {
            address = "172.x.x.x/24";

            web01 [address = "172.x.x.1"];
            web02 [address = "172.x.x.2"];
            db01;
            db02;
          }
        }


#### Commit Graph Diagrams

`kroki-pikchr`:

```kroki-pikchr
scale = 0.8
fill = white
linewid *= 0.5
circle "C0" fit
circlerad = previous.radius
arrow
circle "C1"
arrow
circle "C2"
arrow
circle "C4"
arrow
circle "C6"
circle "C3" at dist(C2,C4) heading 30 from C2
arrow
circle "C5"
arrow from C2 to C3 chop
C3P: circle "C3'" at dist(C4,C6) heading 30 from C6
arrow right from C3P.e
C5P: circle "C5'"
arrow from C6 to C3P chop
```

??? example "Code"

        scale = 0.8
        fill = white
        linewid *= 0.5
        circle "C0" fit
        circlerad = previous.radius
        arrow
        circle "C1"
        arrow
        circle "C2"
        arrow
        circle "C4"
        arrow
        circle "C6"
        circle "C3" at dist(C2,C4) heading 30 from C2
        arrow
        circle "C5"
        arrow from C2 to C3 chop
        C3P: circle "C3'" at dist(C4,C6) heading 30 from C6
        arrow right from C3P.e
        C5P: circle "C5'"
        arrow from C6 to C3P chop

#### Entity Relationship Diagrams

`kroki-erd`:

```kroki-erd
[Person]
*name
height
weight
+birth_location_id

[Location]
*id
city
state
country

Person *--1 Location
```

??? example "Code"

        [Person]
        *name
        height
        weight
        +birth_location_id

        [Location]
        *id
        city
        state
        country

        Person *--1 Location


#### Use Case Diagrams

`kroki-plantuml`:

```kroki-plantuml
@startuml
left to right direction
skinparam packageStyle rectangle
skinparam monochrome true
actor customer
actor clerk
rectangle checkout {
  customer -- (checkout)
  (checkout) .> (payment) : include
  (help) .> (checkout) : extends
  (checkout) -- clerk
}
@enduml
```

??? example "Code"

        @startuml
        left to right direction
        skinparam packageStyle rectangle
        skinparam monochrome true
        actor customer
        actor clerk
        rectangle checkout {
          customer -- (checkout)
          (checkout) .> (payment) : include
          (help) .> (checkout) : extends
          (checkout) -- clerk
        }
        @enduml


#### UML Diagrams

`kroki-nomnoml`:

```kroki-nomnoml
[<abstract>Marauder]<:--[Pirate]
[Pirate]- 0..7[mischief]
[jollyness]->[Pirate]
[jollyness]->[rum]
[jollyness]->[singing]
[Pirate]-> *[rum|tastiness: Int|swig()]
[Pirate]->[singing]
[singing]<->[rum]

[<start>st]->[<state>plunder]
[plunder]->[<choice>more loot]
[more loot]->[st]
[more loot] no ->[<end>e]

[<actor>Sailor] - [<usecase>shiver me;timbers]
```

??? example "Code"

        [<abstract>Marauder]<:--[Pirate]
        [Pirate]- 0..7[mischief]
        [jollyness]->[Pirate]
        [jollyness]->[rum]
        [jollyness]->[singing]
        [Pirate]-> *[rum|tastiness: Int|swig()]
        [Pirate]->[singing]
        [singing]<->[rum]

        [<start>st]->[<state>plunder]
        [plunder]->[<choice>more loot]
        [more loot]->[st]
        [more loot] no ->[<end>e]

        [<actor>Sailor] - [<usecase>shiver me;timbers]


#### Sequence Diagrams

`kroki-mermaid`:

```kroki-mermaid
sequenceDiagram
  participant Alice
  participant Bob
  Alice->John: Hello John, how are you?
  loop Healthcheck
      John->John: Fight against hypochondria
  end
  Note right of John: Rational thoughts prevail...
  John-->Alice: Great!
  John->Bob: How about you?
  Bob-->John: Jolly good!
```

??? example "Code"

        sequenceDiagram
          participant Alice
          participant Bob
          Alice->John: Hello John, how are you?
          loop Healthcheck
              John->John: Fight against hypochondria
          end
          Note right of John: Rational thoughts prevail...
          John-->Alice: Great!
          John->Bob: How about you?
          Bob-->John: Jolly good!

`kroki-seqdiag`:

```kroki-seqdiag
seqdiag {
  browser  -> webserver [label = "GET /index.html"];
  browser <-- webserver;
  browser  -> webserver [label = "POST /blog/comment"];
  webserver  -> database [label = "INSERT comment"];
  webserver <-- database;
  browser <-- webserver;
}
```

??? example "Code"

        seqdiag {
          browser  -> webserver [label = "GET /index.html"];
          browser <-- webserver;
          browser  -> webserver [label = "POST /blog/comment"];
          webserver  -> database [label = "INSERT comment"];
          webserver <-- database;
          browser <-- webserver;
        }


#### World Cloud Diagrams

`kroki-vega`:

```kroki-vega
{
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "width": 800,
  "height": 400,
  "padding": 0,

  "data": [
    {
      "name": "table",
      "values": [
        "Declarative visualization grammars can accelerate development, facilitate retargeting across platforms, and allow language-level optimizations. However, existing declarative visualization languages are primarily concerned with visual encoding, and rely on imperative event handlers for interactive behaviors. In response, we introduce a model of declarative interaction design for data visualizations. Adopting methods from reactive programming, we model low-level events as composable data streams from which we form higher-level semantic signals. Signals feed predicates and scale inversions, which allow us to generalize interactive selections at the level of item geometry (pixels) into interactive queries over the data domain. Production rules then use these queries to manipulate the visualization’s appearance. To facilitate reuse and sharing, these constructs can be encapsulated as named interactors: standalone, purely declarative specifications of interaction techniques. We assess our model’s feasibility and expressivity by instantiating it with extensions to the Vega visualization grammar. Through a diverse range of examples, we demonstrate coverage over an established taxonomy of visualization interaction techniques.",
        "We present Reactive Vega, a system architecture that provides the first robust and comprehensive treatment of declarative visual and interaction design for data visualization. Starting from a single declarative specification, Reactive Vega constructs a dataflow graph in which input data, scene graph elements, and interaction events are all treated as first-class streaming data sources. To support expressive interactive visualizations that may involve time-varying scalar, relational, or hierarchical data, Reactive Vega’s dataflow graph can dynamically re-write itself at runtime by extending or pruning branches in a data-driven fashion. We discuss both compile- and run-time optimizations applied within Reactive Vega, and share the results of benchmark studies that indicate superior interactive performance to both D3 and the original, non-reactive Vega system.",
        "We present Vega-Lite, a high-level grammar that enables rapid specification of interactive data visualizations. Vega-Lite combines a traditional grammar of graphics, providing visual encoding rules and a composition algebra for layered and multi-view displays, with a novel grammar of interaction. Users specify interactive semantics by composing selections. In Vega-Lite, a selection is an abstraction that defines input event processing, points of interest, and a predicate function for inclusion testing. Selections parameterize visual encodings by serving as input data, defining scale extents, or by driving conditional logic. The Vega-Lite compiler automatically synthesizes requisite data flow and event handling logic, which users can override for further customization. In contrast to existing reactive specifications, Vega-Lite selections decompose an interaction design into concise, enumerable semantic units. We evaluate Vega-Lite through a range of examples, demonstrating succinct specification of both customized interaction methods and common techniques such as panning, zooming, and linked selection."
      ],
      "transform": [
        {
          "type": "countpattern",
          "field": "data",
          "case": "upper",
          "pattern": "[\\w']{3,}",
          "stopwords": "(i|me|my|myself|we|us|our|ours|ourselves|you|your|yours|yourself|yourselves|he|him|his|himself|she|her|hers|herself|it|its|itself|they|them|their|theirs|themselves|what|which|who|whom|whose|this|that|these|those|am|is|are|was|were|be|been|being|have|has|had|having|do|does|did|doing|will|would|should|can|could|ought|i'm|you're|he's|she's|it's|we're|they're|i've|you've|we've|they've|i'd|you'd|he'd|she'd|we'd|they'd|i'll|you'll|he'll|she'll|we'll|they'll|isn't|aren't|wasn't|weren't|hasn't|haven't|hadn't|doesn't|don't|didn't|won't|wouldn't|shan't|shouldn't|can't|cannot|couldn't|mustn't|let's|that's|who's|what's|here's|there's|when's|where's|why's|how's|a|an|the|and|but|if|or|because|as|until|while|of|at|by|for|with|about|against|between|into|through|during|before|after|above|below|to|from|up|upon|down|in|out|on|off|over|under|again|further|then|once|here|there|when|where|why|how|all|any|both|each|few|more|most|other|some|such|no|nor|not|only|own|same|so|than|too|very|say|says|said|shall)"
        },
        {
          "type": "formula", "as": "angle",
          "expr": "[-45, 0, 45][~~(random() * 3)]"
        },
        {
          "type": "formula", "as": "weight",
          "expr": "if(datum.text=='VEGA', 600, 300)"
        }
      ]
    }
  ],

  "scales": [
    {
      "name": "color",
      "type": "ordinal",
      "domain": {"data": "table", "field": "text"},
      "range": ["#d5a928", "#652c90", "#939597"]
    }
  ],

  "marks": [
    {
      "type": "text",
      "from": {"data": "table"},
      "encode": {
        "enter": {
          "text": {"field": "text"},
          "align": {"value": "center"},
          "baseline": {"value": "alphabetic"},
          "fill": {"scale": "color", "field": "text"}
        },
        "update": {
          "fillOpacity": {"value": 1}
        },
        "hover": {
          "fillOpacity": {"value": 0.5}
        }
      },
      "transform": [
        {
          "type": "wordcloud",
          "size": [800, 400],
          "text": {"field": "text"},
          "rotate": {"field": "datum.angle"},
          "font": "Helvetica Neue, Arial",
          "fontSize": {"field": "datum.count"},
          "fontWeight": {"field": "datum.weight"},
          "fontSizeRange": [12, 56],
          "padding": 2
        }
      ]
    }
  ]
}
```

??? example "Code"

        {
          "$schema": "https://vega.github.io/schema/vega/v5.json",
          "width": 800,
          "height": 400,
          "padding": 0,

          "data": [
            {
              "name": "table",
              "values": [
                "Declarative visualization grammars can accelerate development, facilitate retargeting across platforms, and allow language-level optimizations. However, existing declarative visualization languages are primarily concerned with visual encoding, and rely on imperative event handlers for interactive behaviors. In response, we introduce a model of declarative interaction design for data visualizations. Adopting methods from reactive programming, we model low-level events as composable data streams from which we form higher-level semantic signals. Signals feed predicates and scale inversions, which allow us to generalize interactive selections at the level of item geometry (pixels) into interactive queries over the data domain. Production rules then use these queries to manipulate the visualization’s appearance. To facilitate reuse and sharing, these constructs can be encapsulated as named interactors: standalone, purely declarative specifications of interaction techniques. We assess our model’s feasibility and expressivity by instantiating it with extensions to the Vega visualization grammar. Through a diverse range of examples, we demonstrate coverage over an established taxonomy of visualization interaction techniques.",
                "We present Reactive Vega, a system architecture that provides the first robust and comprehensive treatment of declarative visual and interaction design for data visualization. Starting from a single declarative specification, Reactive Vega constructs a dataflow graph in which input data, scene graph elements, and interaction events are all treated as first-class streaming data sources. To support expressive interactive visualizations that may involve time-varying scalar, relational, or hierarchical data, Reactive Vega’s dataflow graph can dynamically re-write itself at runtime by extending or pruning branches in a data-driven fashion. We discuss both compile- and run-time optimizations applied within Reactive Vega, and share the results of benchmark studies that indicate superior interactive performance to both D3 and the original, non-reactive Vega system.",
                "We present Vega-Lite, a high-level grammar that enables rapid specification of interactive data visualizations. Vega-Lite combines a traditional grammar of graphics, providing visual encoding rules and a composition algebra for layered and multi-view displays, with a novel grammar of interaction. Users specify interactive semantics by composing selections. In Vega-Lite, a selection is an abstraction that defines input event processing, points of interest, and a predicate function for inclusion testing. Selections parameterize visual encodings by serving as input data, defining scale extents, or by driving conditional logic. The Vega-Lite compiler automatically synthesizes requisite data flow and event handling logic, which users can override for further customization. In contrast to existing reactive specifications, Vega-Lite selections decompose an interaction design into concise, enumerable semantic units. We evaluate Vega-Lite through a range of examples, demonstrating succinct specification of both customized interaction methods and common techniques such as panning, zooming, and linked selection."
              ],
              "transform": [
                {
                  "type": "countpattern",
                  "field": "data",
                  "case": "upper",
                  "pattern": "[\\w']{3,}",
                  "stopwords": "(i|me|my|myself|we|us|our|ours|ourselves|you|your|yours|yourself|yourselves|he|him|his|himself|she|her|hers|herself|it|its|itself|they|them|their|theirs|themselves|what|which|who|whom|whose|this|that|these|those|am|is|are|was|were|be|been|being|have|has|had|having|do|does|did|doing|will|would|should|can|could|ought|i'm|you're|he's|she's|it's|we're|they're|i've|you've|we've|they've|i'd|you'd|he'd|she'd|we'd|they'd|i'll|you'll|he'll|she'll|we'll|they'll|isn't|aren't|wasn't|weren't|hasn't|haven't|hadn't|doesn't|don't|didn't|won't|wouldn't|shan't|shouldn't|can't|cannot|couldn't|mustn't|let's|that's|who's|what's|here's|there's|when's|where's|why's|how's|a|an|the|and|but|if|or|because|as|until|while|of|at|by|for|with|about|against|between|into|through|during|before|after|above|below|to|from|up|upon|down|in|out|on|off|over|under|again|further|then|once|here|there|when|where|why|how|all|any|both|each|few|more|most|other|some|such|no|nor|not|only|own|same|so|than|too|very|say|says|said|shall)"
                },
                {
                  "type": "formula", "as": "angle",
                  "expr": "[-45, 0, 45][~~(random() * 3)]"
                },
                {
                  "type": "formula", "as": "weight",
                  "expr": "if(datum.text=='VEGA', 600, 300)"
                }
              ]
            }
          ],

          "scales": [
            {
              "name": "color",
              "type": "ordinal",
              "domain": {"data": "table", "field": "text"},
              "range": ["#d5a928", "#652c90", "#939597"]
            }
          ],

          "marks": [
            {
              "type": "text",
              "from": {"data": "table"},
              "encode": {
                "enter": {
                  "text": {"field": "text"},
                  "align": {"value": "center"},
                  "baseline": {"value": "alphabetic"},
                  "fill": {"scale": "color", "field": "text"}
                },
                "update": {
                  "fillOpacity": {"value": 1}
                },
                "hover": {
                  "fillOpacity": {"value": 0.5}
                }
              },
              "transform": [
                {
                  "type": "wordcloud",
                  "size": [800, 400],
                  "text": {"field": "text"},
                  "rotate": {"field": "datum.angle"},
                  "font": "Helvetica Neue, Arial",
                  "fontSize": {"field": "datum.count"},
                  "fontWeight": {"field": "datum.weight"},
                  "fontSizeRange": [12, 56],
                  "padding": 2
                }
              ]
            }
          ]
        }


### Footnotes

#### Single-line

Lorem ipsum[^1] dolor sit amet, consectetur adipiscing elit.

[^1]: Lorem ipsum dolor sit amet, consectetur adipiscing elit.


??? example "Code"

    Define anywhere in text:
    
        Lorem ipsum[^1] dolor sit amet, consectetur adipiscing elit.

    And add the explanation afterwards:

        [^1]: Lorem ipsum dolor sit amet, consectetur adipiscing elit. 

#### Multi-line

Lorem ipsum dolor sit amet, consectetur adipiscing elit[^2].

[^2]:
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.


??? example "Code"

    Define anywhere in text:
    
        Lorem ipsum dolor sit amet, consectetur adipiscing elit[^2].

    With multi-line, we need to add a newline and 4 spaces before writing the explanation:

        [^2]:
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. 


### Grids

#### Generic

We can create grids by encapsulate elements in a `<div>` tag, with `class="grid"` for wrapping grid elements and `markdown` for markdown support. Generic grids allow for arranging arbitrary block elements in a grid, including callouts, code blocks, content tabs and more.

<div class="grid" markdown>

=== "Unordered list"

    * Sed sagittis eleifend rutrum
    * Donec vitae suscipit est
    * Nulla tempor lobortis orci

=== "Ordered list"

    1. Sed sagittis eleifend rutrum
    2. Donec vitae suscipit est
    3. Nulla tempor lobortis orci

``` title="Content tabs"
=== "Unordered list"

    * Sed sagittis eleifend rutrum
    * Donec vitae suscipit est
    * Nulla tempor lobortis orci

=== "Ordered list"

    1. Sed sagittis eleifend rutrum
    2. Donec vitae suscipit est
    3. Nulla tempor lobortis orci
```

</div>

??? example "Code"

        <div class="grid" markdown>

        === "Unordered list"

            * Sed sagittis eleifend rutrum
            * Donec vitae suscipit est
            * Nulla tempor lobortis orci

        === "Ordered list"

            1. Sed sagittis eleifend rutrum
            2. Donec vitae suscipit est
            3. Nulla tempor lobortis orci

        ``` title="Content tabs"
        === "Unordered list"

            * Sed sagittis eleifend rutrum
            * Donec vitae suscipit est
            * Nulla tempor lobortis orci

        === "Ordered list"

            1. Sed sagittis eleifend rutrum
            2. Donec vitae suscipit est
            3. Nulla tempor lobortis orci
        ```

        </div>

#### Cards

Define each card in a list. By including `markdown` in the `<div>` tag, we can utilize markdown in each card as well.

##### Simple Example

<div class="grid cards" markdown>

- :fontawesome-brands-html5: __HTML__ for content and structure
- :fontawesome-brands-js: __JavaScript__ for interactivity
- :fontawesome-brands-css3: __CSS__ for text running out of boxes
- :fontawesome-brands-internet-explorer: __Internet Explorer__ ... huh?

</div>

??? example "Code"

        <div class="grid cards" markdown>

        - :fontawesome-brands-html5: __HTML__ for content and structure
        - :fontawesome-brands-js: __JavaScript__ for interactivity
        - :fontawesome-brands-css3: __CSS__ for text running out of boxes
        - :fontawesome-brands-internet-explorer: __Internet Explorer__ ... huh?

        </div>

##### Advanced Example

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Set up in 5 minutes__

    ---

    Install [`mkdocs-material`](#) with [`pip`](#) and get up
    and running in minutes

    [:octicons-arrow-right-24: Getting started](#)

-   :fontawesome-brands-markdown:{ .lg .middle } __It's just Markdown__

    ---

    Focus on your content and generate a responsive and searchable static site

    [:octicons-arrow-right-24: Reference](#)

-   :material-format-font:{ .lg .middle } __Made to measure__

    ---

    Change the colors, fonts, language, icons, logo and more with a few lines

    [:octicons-arrow-right-24: Customization](#)

-   :material-scale-balance:{ .lg .middle } __Open Source, MIT__

    ---

    Material for MkDocs is licensed under MIT and available on GitHub

    [:octicons-arrow-right-24: License](#)

</div>

??? example "Code"

        <div class="grid cards" markdown>

        -   :material-clock-fast:{ .lg .middle } __Set up in 5 minutes__

            ---

            Install [`mkdocs-material`](#) with [`pip`](#) and get up
            and running in minutes

            [:octicons-arrow-right-24: Getting started](#)

        -   :fontawesome-brands-markdown:{ .lg .middle } __It's just Markdown__

            ---

            Focus on your content and generate a responsive and searchable static site

            [:octicons-arrow-right-24: Reference](#)

        -   :material-format-font:{ .lg .middle } __Made to measure__

            ---

            Change the colors, fonts, language, icons, logo and more with a few lines

            [:octicons-arrow-right-24: Customization](#)

        -   :material-scale-balance:{ .lg .middle } __Open Source, MIT__

            ---

            Material for MkDocs is licensed under MIT and available on GitHub

            [:octicons-arrow-right-24: License](#)

        </div>



### Iconography

For searching through all available icons, use the search functionality [here](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/#search).

**Emojies**

:smile:

**Font Awesome**

:fontawesome-regular-face-laugh-wink:

**Material Design**

:material-at:

**Octicons**

:octicons-log-16:

**Simple Icons**

:simple-ea:

??? example "Code"

        **Emojies**

        :smile:

        **Font Awesome**

        :fontawesome-regular-face-laugh-wink:

        **Material Design**

        :material-at:

        **Octicons**

        :octicons-log-16:

        **Simple Icons**

        :simple-ea:

### Images

#### Default format

This is a default image with defined dark and light mode variants. Simply remove the `#only-light` or `#only-dark` tag to disable the corresponding mode. The caption can also be removed. For style properties (e.g., `width=400`), write them in curly braces at the end, each separated by a semicolon.

<figure markdown="span">
    ![Illustration image, light mode](https://squidfunk.github.io/mkdocs-material/assets/images/zelda-light-world.png#only-light){ width="400"}
    ![Illustration image, dark mode](https://squidfunk.github.io/mkdocs-material/assets/images/zelda-dark-world.png#only-dark){ width="400" }
    <figcaption>Image caption</figcaption>
</figure>

> We could have defined align="center", but this is default and has no effect.

??? example "Code"

        <figure markdown="span">
            ![Illustration image, light mode](https://squidfunk.github.io/mkdocs-material/assets/images/zelda-light-world.png#only-light){ width="400"}
            ![Illustration image, dark mode](https://squidfunk.github.io/mkdocs-material/assets/images/zelda-dark-world.png#only-dark){ width="400" }
            <figcaption>Image caption</figcaption>
        </figure>

#### Alignment

=== "Center"

    **Default**

    ![Illustration](https://squidfunk.github.io/mkdocs-material/assets/images/zelda-light-world.png){ width="250" }

    **To align in center of div, use `<figure markdown="span"></figure>`.**

    <figure markdown="span">
        ![Illustration image, light mode](https://squidfunk.github.io/mkdocs-material/assets/images/zelda-light-world.png){ width="250" }
    </figure>

    ??? example "Code"

        ```
        **Default**

        ![Illustration](https://squidfunk.github.io/mkdocs-material/assets/images/zelda-light-world.png){ width="250" }

        **To align in center of div, use `<figure markdown="span"></figure>`.**

        <figure>
            ![Illustration image, light mode](https://squidfunk.github.io/mkdocs-material/assets/images/zelda-light-world.png){ width="250" }
        </figure>
        ```

=== "Left"

    ![Illustration](https://squidfunk.github.io/mkdocs-material/assets/images/zelda-light-world.png){ align="left"; width="250" }

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa, nec semper lorem quam in massa. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa, nec semper lorem quam in massa. Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    ??? example "Code"

        ```
        ![Illustration](https://squidfunk.github.io/mkdocs-material/assets/images/zelda-light-world.png){ align="left"; width="250" }

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa, nec semper lorem quam in massa. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa, nec semper lorem quam in massa.
        ```

=== "Right"

    ![Illustration](https://squidfunk.github.io/mkdocs-material/assets/images/zelda-light-world.png){ align="right"; width="250" }

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa, nec semper lorem quam in massa. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa, nec semper lorem quam in massa. Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    ??? example "Code"

        ```
        ![Illustration](https://squidfunk.github.io/mkdocs-material/assets/images/zelda-light-world.png){ align="right"; width="250" }

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa, nec semper lorem quam in massa. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa, nec semper lorem quam in massa.
        ```




### Lists

#### Unordered

- Nulla et rhoncus turpis. Mauris ultricies elementum leo. Duis efficitur
  accumsan nibh eu mattis. Vivamus tempus velit eros, porttitor placerat nibh
  lacinia sed. Aenean in finibus diam.

    * Duis mollis est eget nibh volutpat, fermentum aliquet dui mollis.
    * Nam vulputate tincidunt fringilla.
    * Nullam dignissim ultrices urna non auctor.

??? example "Code"

        - Nulla et rhoncus turpis. Mauris ultricies elementum leo. Duis efficitur
          accumsan nibh eu mattis. Vivamus tempus velit eros, porttitor placerat nibh
          lacinia sed. Aenean in finibus diam.

            * Duis mollis est eget nibh volutpat, fermentum aliquet dui mollis.
            * Nam vulputate tincidunt fringilla.
            * Nullam dignissim ultrices urna non auctor.

#### Ordered

1.  Vivamus id mi enim. Integer id turpis sapien. Ut condimentum lobortis
    sagittis. Aliquam purus tellus, faucibus eget urna at, iaculis venenatis
    nulla. Vivamus a pharetra leo.

    1.  Vivamus venenatis porttitor tortor sit amet rutrum. Pellentesque aliquet
        quam enim, eu volutpat urna rutrum a. Nam vehicula nunc mauris, a
        ultricies libero efficitur sed.

    2.  Morbi eget dapibus felis. Vivamus venenatis porttitor tortor sit amet
        rutrum. Pellentesque aliquet quam enim, eu volutpat urna rutrum a.

        1.  Mauris dictum mi lacus
        2.  Ut sit amet placerat ante
        3.  Suspendisse ac eros arcu
   
??? example "Code"

        1.  Vivamus id mi enim. Integer id turpis sapien. Ut condimentum lobortis
            sagittis. Aliquam purus tellus, faucibus eget urna at, iaculis venenatis
            nulla. Vivamus a pharetra leo.

            1.  Vivamus venenatis porttitor tortor sit amet rutrum. Pellentesque aliquet
                quam enim, eu volutpat urna rutrum a. Nam vehicula nunc mauris, a
                ultricies libero efficitur sed.

            2.  Morbi eget dapibus felis. Vivamus venenatis porttitor tortor sit amet
                rutrum. Pellentesque aliquet quam enim, eu volutpat urna rutrum a.

                1.  Mauris dictum mi lacus
                2.  Ut sit amet placerat ante
                3.  Suspendisse ac eros arcu

#### Definitions

`Lorem ipsum dolor sit amet`

:   Sed sagittis eleifend rutrum. Donec vitae suscipit est. Nullam tempus
    tellus non sem sollicitudin, quis rutrum leo facilisis.

`Cras arcu libero`

:   Aliquam metus eros, pretium sed nulla venenatis, faucibus auctor ex. Proin
    ut eros sed sapien ullamcorper consequat. Nunc ligula ante.

    Duis mollis est eget nibh volutpat, fermentum aliquet dui mollis.
    Nam vulputate tincidunt fringilla.
    Nullam dignissim ultrices urna non auctor.

??? example "Code"

        `Lorem ipsum dolor sit amet`

        :   Sed sagittis eleifend rutrum. Donec vitae suscipit est. Nullam tempus
            tellus non sem sollicitudin, quis rutrum leo facilisis.

        `Cras arcu libero`

        :   Aliquam metus eros, pretium sed nulla venenatis, faucibus auctor ex. Proin
            ut eros sed sapien ullamcorper consequat. Nunc ligula ante.

            Duis mollis est eget nibh volutpat, fermentum aliquet dui mollis.
            Nam vulputate tincidunt fringilla.
            Nullam dignissim ultrices urna non auctor.

#### Tasks

- [x] Lorem ipsum dolor sit amet, consectetur adipiscing elit
- [ ] Vestibulum convallis sit amet nisi a tincidunt
    * [x] In hac habitasse platea dictumst
    * [x] In scelerisque nibh non dolor mollis congue sed et metus
    * [ ] Praesent sed risus massa
- [ ] Aenean pretium efficitur erat, donec pharetra, ligula non scelerisque

??? example "Code"

        - [x] Lorem ipsum dolor sit amet, consectetur adipiscing elit
        - [ ] Vestibulum convallis sit amet nisi a tincidunt
            * [x] In hac habitasse platea dictumst
            * [x] In scelerisque nibh non dolor mollis congue sed et metus
            * [ ] Praesent sed risus massa
        - [ ] Aenean pretium efficitur erat, donec pharetra, ligula non scelerisque


### Math

Using [MathJax](https://www.mathjax.org/), we support [LaTeX](https://www.latex-project.org/), [MathML](https://w3c.github.io/mathml/), [AsciiMath](https://asciimath.org/), as well as output formats like HTML, SVG, MathML. 

#### Block Syntax

Blocks must be enclosed in `$$...$$` or `\[...\]` on separate lines:

$$
\operatorname{ker} f=\{g\in G:f(g)=e_{H}\}{\mbox{.}}
$$

??? example "Code"

    **Standard**

        $$
        \operatorname{ker} f=\{g\in G:f(g)=e_{H}\}{\mbox{.}}
        $$

    **Alternative**

        \[
        \operatorname{ker} f=\{g\in G:f(g)=e_{H}\}{\mbox{.}}
        \]

#### Inline Block Syntax

Inline blocks must be enclosed in `$...$` or `\(...\)`:

The homomorphism $f$ is injective if and only if its kernel is only the
singleton set $e_G$, because otherwise $\exists a,b\in G$ with $a\neq b$ such
that \(f(a)=f(b)\).

??? example "Code"

        The homomorphism $f$ is injective if and only if its kernel is only the
        singleton set $e_G$, because otherwise $\exists a,b\in G$ with $a\neq b$ such
        that \(f(a)=f(b)\).
    


### Tables

#### Default

| Method   | Description                          |
| -------- | ------------------------------------ |
| `GET`    | :material-check:     Fetch resource  |
| `PUT`    | :material-check-all: Update resource |
| `DELETE` | :material-close:     Delete resource |

??? example "Code"

        | Method   | Description                          |
        | -------- | ------------------------------------ |
        | `GET`    | :material-check:     Fetch resource  |
        | `PUT`    | :material-check-all: Update resource |
        | `DELETE` | :material-close:     Delete resource |

#### Alignment

=== "Left"

    | Method   | Description                          |
    | :------- | :----------------------------------- |
    | `GET`    | :material-check:     Fetch resource  |
    | `PUT`    | :material-check-all: Update resource |
    | `DELETE` | :material-close:     Delete resource |


    ??? example "Code"
    
        ```hl_lines="2"
        | Method   | Description                          |
        | :------- | :----------------------------------- |
        | `GET`    | :material-check:     Fetch resource  |
        | `PUT`    | :material-check-all: Update resource |
        | `DELETE` | :material-close:     Delete resource |
        ```

=== "Center"

    |  Method  |             Description              |
    | :------: | :----------------------------------: |
    |  `GET`   | :material-check:     Fetch resource  |
    |  `PUT`   | :material-check-all: Update resource |
    | `DELETE` | :material-close:     Delete resource |


    ??? example "Code"

        ```hl_lines="2"
        |  Method  |             Description              |
        | :------: | :----------------------------------: |
        |  `GET`   | :material-check:     Fetch resource  |
        |  `PUT`   | :material-check-all: Update resource |
        | `DELETE` | :material-close:     Delete resource |
        ```

=== "Right"

    |   Method |                          Description |
    | -------: | -----------------------------------: |
    |    `GET` |  :material-check:     Fetch resource |
    |    `PUT` | :material-check-all: Update resource |
    | `DELETE` | :material-close:     Delete resource |


    ??? example "Code"

        ```hl_lines="2"
        |   Method |                          Description |
        | -------: | -----------------------------------: |
        |    `GET` |  :material-check:     Fetch resource |
        |    `PUT` | :material-check-all: Update resource |
        | `DELETE` | :material-close:     Delete resource |
        ```

### Text

#### Default

By default, we can use the formating of Markdown. This includes **bold**, *italic* and <ins>underlined</ins> text. Additionally, one can add [links](../index.md) and `inline code`.

??? example "Code"

    ```
    By default, we can use the formating of Markdown. This includes **bold**, *italic* and <ins>underlined</ins> text. Additionally, one can add [links](../index.md) and `inline code`.
    ```

#### Formatting

##### Highlighting Changes

Text can be {--deleted--} and replacement text {++added++}. This can also be
combined into {~~one~>a single~~} operation. {==Highlighting==} is also
possible {>>and comments can be added inline<<}.

{==

Formatting can also be applied to blocks by putting the opening and closing
tags on separate lines and adding new lines between the tags and the content.

==}

??? example "Code"

        All needs to be encapsulated in curly braces!

        Deleted: `--deleted--`
        Replaced: `++added`++`
        Oneline: `~~one~>a single~~`
        Highlight: `==Highlighting==`
        Comments: `>>inline comment<<`
        Block highlight: `== \n <block of text> \n ==`
    

##### Highlighting Text

- ==This was marked==
- ^^This was inserted^^
- ~~This was deleted~~

??? example "Code"

        - ==This was marked==
        - ^^This was inserted^^
        - ~~This was deleted~~

##### Sub- and Superscripts

- Subsript: H~2~O
- Superscript: A^T^A

??? example "Code"

        - Subsript: H~2~O
        - Superscript: A^T^A    

##### Keyboard Keys

++ctrl+alt+del++

??? example "Code"

        ++ctrl+alt+del++


### Tooltips

#### Links

**Inline syntax**

[Hover me](https://example.com "I'm a tooltip!")

??? example "Code"

        [Hover me](https://example.com "I'm a tooltip!")

**Reference Syntax**

[Hover me][example]

  [example]: https://example.com "I'm a tooltip!"

??? example "Code"

        [Hover me][example]

          [example]: https://example.com "I'm a tooltip!"


#### Additional Elements

Can also add tooltips to other elements by using the attribute list extension (here with icon):

:material-information-outline:{ title="Important information" }

??? example "Code"

        :material-information-outline:{ title="Important information" }

#### Abbreviations

Abbreviations can be defined by using a special syntax similar to URLs and footnotes, starting with a `*` and immediately followed by the term or acronym to be associated in square brackets:

The HTML specification is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium

??? example "Code"

        The HTML specification is maintained by the W3C.

        *[HTML]: Hyper Text Markup Language
        *[W3C]: World Wide Web Consortium

### Quotes

> This is a block quote

??? example "Code"

        > This is a block quote


## Configurables

There are some configurations you might want to be familiar with when writing your documents. Most of these utilize what is known as a **front matter**, that is, a property syntax defined before the first header, which describe some specific rules for the given page. Let's dive in.

### Hiding Sidebar on Specific Page

If you want to hide the navigation and/or table of contents on a document page, you can use a front matter `hide` property as such:

```
---
hide:
  - navigation
  - toc
---

# Page title
...
```

### Boost Page in Search Results

Pages can be given a boost or drop in search ranking with the front matter `search.boost` property:

=== "Rank up"

    ```
    ---
    search:
      boost: 2 
    ---

    # Page title
    ...
    ```

=== "Rank down"

    ```
    ---
    search:
      boost: 0.5 
    ---

    # Page title
    ...
    ```

### Search Exclusion

#### Pages

Pages can be removed from the search index, thus excluding them from search, with the front matter `search.exclude` property:

```
---
search:
  exclude: true
---

# Page title
...
```

#### Sections

Using attribute lists, we can exclude specific sections from the search index with `{ data-search-exclude }` defined in the heading:

```
# Page title

## Section 1

The content of this section is included

## Section 2 { data-search-exclude }

The content of this section is excluded
```

#### Blocks

As with sections, blocks can be excluded from search as well, if using the attribute list in a regular block instead:

```
# Page title

The content of this block is included

The content of this block is excluded
{ data-search-exclude }
```