# Roundtable 2025-01-21
#### N Owen 

## Introduction

For those drowning in information overload, [Obsidian.md](https://obsidian.md/) offers a lifeline. This powerful tool transcends a simple note-taking app, functioning as an effective knowledge management system for documents and events.

>[!NOTE]
> - Your thoughts are yours.
> - Obsidian stores notes on your device, so you can access them quickly, even offline. No one else can read them, not even us.
> - Your mind is unique.
> - With thousands of plugins and themes, you can shape Obsidian to fit your way of thinking.
> - Your knowledge should last.
> - Obsidian uses open, non-proprietary files, so you're never locked in, and can preserve your data for the long term.
> - _copied from Obsidian.md 2025-01-20_


## Benefits

- Non propietry - markdown based documentation thats viewable on pretty much anything
- Non-linear thinking: Unlike traditional note-taking apps, Obsidian is designed for non-linear thinking, enabling a more organic development of ideas.
- Linked notes: One of the best features of Obsidian is its ability to link notes together, creating a web of interconnected information.   
- Customizable: With thousands of plugins and themes, you can shape Obsidian to fit your way of thinking.
- Privacy: Your thoughts are yours. Obsidian stores notes on your device, so you can access them quickly, even offline. 
- Free for personal use

## Creating a new empty vault

To create a new empty vault:

- To the right of `Create new vault`, click `Create`.
- In `Vault name`, enter the name of your vault.
- Click `Browse` to select where your new vault will be created.
- Click `Create`

## Specific Examples of Notes

### Markmap
further info: https://markmap.js.org/repl
```
---
title: markmap
markmap:
  colorFreezeLevel: 2
---

## Links

- [Website](https://markmap.js.org/)
- [GitHub](https://github.com/gera2ld/markmap)

## Related Projects

- [coc-markmap](https://github.com/gera2ld/coc-markmap) for Neovim
- [markmap-vscode](https://marketplace.visualstudio.com/items?itemName=gera2ld.markmap-vscode) for VSCode
- [eaf-markmap](https://github.com/emacs-eaf/eaf-markmap) for Emacs

## Features

Note that if blocks and lists appear at the same level, the lists will be ignored.

### Lists

- **strong** ~~del~~ *italic* ==highlight==
- `inline code`
- [x] checkbox
- Katex: $x = {-b \pm \sqrt{b^2-4ac} \over 2a}$ <!-- markmap: fold -->
  - [More Katex Examples](#?d=gist:af76a4c245b302206b16aec503dbe07b:katex.md)
- Now we can wrap very very very very long text based on `maxWidth` option
- Ordered list
  1. item 1
  2. item 2


| Products | Price |
|-|-|
| Apple | 4 |
| Banana | 2 |

![](https://markmap.js.org/favicon.png)

```
Code for my usage: 

```
# Markmap


```markmap
---
markmap:
  height: 869
---
# Comms

---

## Faculty
### strategy board
- [x] asked for me to present at future meeting 📅 2024-10-11 
- [x] replied 📅 2024-10-11 
- [ ] Meeting confirmed for 09-01-2025⏳ 2025-01-09 🔺  


---

## Project X
- [x] [GitHub Issue](https://github.com/yaddayadda)
- [x] Teams meeting 📅 2024-07-31
- [x] Meeting 📅 2024-09-27
- [x] Outcome: shared [Excel](https://liveuclac-my.sharepoint.com/)
- [x] Contact owners of file shared 📅 2024-10-10 
	- [x] James Dean 
	- [ ] Jim Bob
	- [ ] Sally Swift
	- [ ] Taylor her sister
- [ ] 

---

## Somewhere else
- [x] Contact Billy Bob, Linda
- [x] [GitHub Issue](https://github.com/yadda)
- [x] Email from XXXXX re: YYYYYY on the ZZZZZZZ (JDean)
	- [x] Email from JDean to Taylor Swift to discuss
	- [x] I replied on 0📅 2024-10-02 19:20
	- [x] resolved 


### Another Project
- [x] Contacts :
- [x] Email to meet to discuss requirements 📅 2024-10-09 
	- [x] response: not directly involved but happy to support researchers needs 📅 2024-10-11 
		- [x] replied 📅 2024-10-11 
- [x] Meeting to discuss 📅 2024-10-23
	- [x] Outcomes:
		- [x] New IT Board Established
		- [x] Monthly meetings
		- [ ] Next  📅 2024-11-20 
		- [ ] Report on requirements
- [ ] Gather current requirements in documentation 🔺 
- [x] Email XXXX at XXXX re opportunity to get heard re  usage 🔺
	- [x] Draft sent to Linda and Jim
	- [x] sent out to  📅 2024-11-11
		- [x] responses
			- [x] s 📅 2024-11-13 
				- [ ] followup to discuss TRE/DSH/Compute 🔺 
- [x] Email to XXXXX re: new hardware purchase📅 


### Data Management
- [x] RDSS Statistics for reporting 🔺 
	- [x] Sept 📅 2024-10-01
	- [x] Oct 📅 2024-11-01
	- [x] Nov 📅 2024-12-01
	- [x] Dec 📅 2025-01-01 


```

### Data View
info: https://blacksmithgu.github.io/obsidian-dataview/

Data Indexing example note:
```
---
author: "Edgar Allan Poe"
published: 1845
tags: poems
---

# The Raven

Once upon a midnight dreary, while I pondered, weak and weary,
Over many a quaint and curious volume of forgotten lore—
```

Data Querying example

````
```dataview
LIST
```
````

a more restricted Query:

````
```dataview
LIST
FROM #poems
WHERE author = "Edgar Allan Poe"
```
````


### Examples of My Usage:

Calendar entries: in `/general/calendar`
````
```dataview
table without ID
	link(file.link, title) as "Event", 
	date as "Date", 
	URL as "Link" ,
	formatType as "Format"
from "General/calendar" 
FLATTEN dateformat(date(this.file.day), "EEE") AS wDay 
FLATTEN ((x) => { Mon: "M", Tue: "T", Wed: "W", Thu: "R", Fri: "F", Sat: "S" , Sun: "U" }[x])(wDay) AS sDay 
where 
	contains(daysOfWeek, sDay) 
	or 
	file.day = this.file.day 
	and
	file.name !="_Index_of_calendar"
sort startTime ASC
```
````


Outstanding tasks:<br>
A task starts with `- [ ] ` check box entry to make simply either done with `x` or not done ` `
````
```tasks 
starts on or after 2024-01-01
not done 
```
````

Tag Summary:<br>

````
```dataview
TABLE
		length(rows.file.name) as entries
	, join(rows.file.link, ", ") as files
FROM
		#ion or #meeting 
flatten
		file.tags as tag
group by
		tag
		
SORT entries DESC
```
````

#### Useful Plugins
##### Admonitions
https://plugins.javalent.com/admonitions/beginner/types
examples
````
```ad-note
title: Nested Admonitions
collapse: open

Hello!
```
````

````
```ad-danger
Warning this wont work
```
````

````
```ad-info
Hello this is a useful bit of informatrion. 
```
````

##### Obsidian Calendar
https://github.com/liamcain/obsidian-calendar-plugin

##### Homepage
https://github.com/mirnovov/obsidian-homepage
Sets a default page on start

##### Mindmap
https://github.com/lynchjames/obsidian-mind-map
Create the markmaps and various mindmap styles

##### DataView
https://github.com/blacksmithgu/obsidian-dataview

##### File Tree Alternative
https://github.com/ozntel/file-tree-alternative

##### Table of Contents
https://github.com/hipstersmoothie/obsidian-plugin-toc

##### Tasks
https://github.com/obsidian-tasks-group/obsidian-tasks
examples:
````
- [ ] Something non-important, with no date
- [ ] Remember to do that important thing - with a due date 📅 2022-12-17
- [ ] Send Kate a birthday card - with a scheduled date 🔁 every January on the 4th ⏳ 2023-01-04
````

````
```tasks
# Only tasks that are not done, that is, which begin like this (but without the quotes):
#   '- [ ] ' or
#   '* [ ] ' or
#   '1. [ ] '
# Indented tasks are supported, but only single-line tasks.
not done

# Tasks due today or earlier:
due before tomorrow

# Restrict to at most 100 tasks.
# If you ask Tasks to display many hundreds or thousands of tasks,
# Obsidian's editing performance really slows down.
limit 100

# Group and sort the output:
group by filename
sort by due reverse
sort by description

# Optionally, ask Tasks to explain how it interpreted this query:
explain
```
````

