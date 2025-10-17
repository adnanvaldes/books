from typing import  Dict

def tabulate(books:Dict):
    headers = ["id","title","author","finish_date"]
    col_widths={h:len(str(h)) for h in headers}#this will make a dictionary where {header1:its length,header2 :its length}
    for book in books:
        for header in headers:
            cell=str(getattr(book,header))
            col_widths[header]=max(len(cell),col_widths[header])
    #by the end of this loop the col_widths will have the maximum length of any cell within each different column
    header_row=(" | ").join(str(h).ljust(col_widths[h])for h in headers)
    #this adjusts the headers such that spaces are added so the length of the header matches its coresponding max lenght value form col_widths
    
    lines=[]
    lines.append(header_row)
    
    seperator = "-+-".join("-"* col_widths[h] for h in headers)
    lines.append(seperator)
    
    for book in books:
        line=" | ".join(str(getattr(book,h)).ljust(col_widths[h]) for h in headers)
        lines.append(line)
        
    return "\n".join(lines)