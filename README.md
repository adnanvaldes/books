Fields:
```
| SN  | Title | Author | Format | P.date | Pagecount | runtime | S.date | E.date|
|-----|-------|--------|--------|--------|-----------|---------|--------|-------|
|     |       |        |        |        |           |         |        |       |
|     |       |        |        |        |           |         |        |       |
--------------------------------------------------------------------------------
```
Title and format should be compulsory , The rest we ask LLMs to find and the user to confirm . In terms of Start date we default to now and end date we default to None.
# Features
##  Basics:
```
book -- delete "Title"
book -- Finish # Updates the E.date to today
book -- Import 
book -- Export <desired_format>
book --edit --name_of_column "value_to_add" 
```

## book --add  usage:
```
book --add --title "The Stranger" --author "Albert Camus" --format "Physical" 

OR

book --add 
1.What is the title of the book?
2.What is the format of the book?(choose one)
	a.Physical
	b.Audiobook
	c.E-book

"""
This is for later after we make a basic one 

Would you like to autocomplete the rest of the entry?(Y/N)
if Y:
	take 1,2 and then autocomplete with an LLM ,Vefiry with user
else :
	Goto Q3	
"""


3.What is the Name of the Author?
4.  ....
5.  ....
   etc 
   etc
```

Aditionally if a user uses book --add with incomplete data then we resort to asking questions for eg :

```

book --add --title "The Republic" --format "E-book"

What is the name of the author?
What is the Publication date?
etc etc 

Essentially the idea is to pick up with questions wherever the user left off with the command.

book --add --title "The Republic" --format"E-book" --autoupdate

# --autoupdate is basically saying do the rest with an LLM.
```

## book --list usage:

```
book --list 
book --list -a "author name" #will list all the books with that authors title 
book --list -g "genre"
book --list -f "format"

#ideally the list function should do multi level filtering too so smth like
book list -a "camus" -f "audiobook" -genre "fiction" 

#little more advanced

book --list --sort #A-Z by default
book --list --sort -pc #by page count
book --list --sort -date
book --list --sort -S.date


#Then we think about something like :
book list -a "camus" -f "audiobook" -genre "fiction" --sort -pc
```

## book -- recap usage:
```
book --recap -a "authorname" and/or -i "[weeks][year][etc]" 

Should diplay something like :

Recap for books from Autohor:name in the past x days/weeks
===============================================
Books read: int
Finished books :
Pending Books :
Total Page count: int
Average Page count : int
Aveage number of days take to finsh a book:
Max no of days taken to finsih a book : days(Title)

# We dont have to show all of this just an example 
```

## Other potential features for the future:
1. $EDITOR ->YAML (make entries into YAML files that can be loaded and edited in any editor)
 ⁠
##  Implementation
SQL backend
Python
Standard library
CLI -> UI