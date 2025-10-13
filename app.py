import loadscreen
import argparse

def add():
	print("add function will be here ")
	return
def edit():
	print("edit function will be here ")
	return
def delete():
	print("delete function will be here ")
	return
def finish():
	print("finish function will be here ")
	return
def Import():
	print("import function will be here ")
	return
def Export():
	print("Export function will be here ")
	return
def list():
	print("list function will be here ")
def recap():
	print("recap function will be here")


def main():
	loadscreen.welcome()
	print("Welcome to Books ")
	print("For help enter : books -h")
	
	parser=argparse.ArgumentParser(prog="book",description="Book manager")

	subparsers=parser.add_subparsers(dest="action",required=True)
	clear_parser = subparsers.add_parser('clear', help='CLS')
	# LIST subcommand
	list_parser = subparsers.add_parser('list', help='List books')

	list_parser.add_argument('-a', '--author', type=str, help='Filter by author')
	list_parser.add_argument('-g', '--genre', type=str, help='Filter by genre')
	list_parser.add_argument('-f', '--format', type=str, help='Filter by format')
	list_parser.add_argument('--sort', nargs='?', const='title', help='Sort results')
	list_parser.add_argument('-pc', '--page-count', action='store_true', help='Sort by page count')
	list_parser.add_argument('-date', '--date', action='store_true', help='Sort by date')
	list_parser.add_argument('-S', '--start-date', action='store_true', help='Sort by start date')
    
    # ADD subcommand
	add_parser = subparsers.add_parser('add', help='Add a book')
	add_parser.add_argument('-a', '--author', type=str, help='Filter by author')
	add_parser.add_argument('-g', '--genre', type=str, help='Filter by genre')
	add_parser.add_argument('-f', '--format', type=str, help='Filter by format')
	add_parser.add_argument('--sort', nargs='?', const='title', help='Sort results')
	add_parser.add_argument('-pc', '--page-count', action='store_true', help='Sort by page count')
	add_parser.add_argument('-date', '--date', action='store_true', help='Sort by date')
	add_parser.add_argument('-S', '--start-date', action='store_true', help='Sort by start date')
    
    # DELETE subcommand
	delete_parser = subparsers.add_parser('delete', help='Delete a book')
	delete_parser.add_argument('title', type=str, help='Book title')
    
    # EDIT subcommand
	edit_parser = subparsers.add_parser('edit', help='Edit a book')
	edit_parser.add_argument('-a', '--author', type=str, help='Filter by author')
	edit_parser.add_argument('-g', '--genre', type=str, help='Filter by genre')
	edit_parser.add_argument('-f', '--format', type=str, help='Filter by format')
	edit_parser.add_argument('--sort', nargs='?', const='title', help='Sort results')
	edit_parser.add_argument('-pc', '--page-count', action='store_true', help='Sort by page count')
	edit_parser.add_argument('-date', '--date', action='store_true', help='Sort by date')
	edit_parser.add_argument('-S', '--start-date', action='store_true', help='Sort by start date')

    # FINISH subcommand
	finish_parser = subparsers.add_parser('finish', help='Mark book as finished')
	while True:
		try:
			user_input=input("> ").strip()
			
			if user_input in ['exit','quit']:
				print("\nThanks for using books")
				break
			if not user_input:
				continue
			
			args = parser.parse_args(user_input.split())

			if args.action == "list":
				list()
			elif args.action == "add":
				add()
			elif args.action =="edit":
				edit()
			elif args.action =="finish":
				finish()
			elif args.action =="delete":
				delete()
			elif args.action =="Import":
				Import()
			elif args.action =="Export":
				Export()
			elif args.action =="recap":
				recap()
			elif args.action =="clear":
				loadscreen.welcome()

		except SystemExit:
			continue
		except KeyboardInterrupt:
			print("\nThanks for using books")
			break

			



if __name__ == "__main__":
	main()