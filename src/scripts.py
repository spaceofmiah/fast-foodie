from db.models.foods import create_food_tables


def create_tables():
	"""Create all application tables"""
	create_food_tables()


if __name__ == "__main__":
	print("Application Database Management")
	print("1. create tables")
	print("2. delete tables")
	choice = int(input("What do you want to do ?: "))

	if choice == 1:
		create_tables()
	elif choice == 2:
		print("nothing to do yet !!!")
