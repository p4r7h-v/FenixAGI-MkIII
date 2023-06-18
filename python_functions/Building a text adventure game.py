def start_game():
    print("Welcome to the Text Adventure!")
    
    while True:
        print("\nYou are in a dark room. There are 3 doors. Which one will you choose?")
        print("1. Red Door")
        print("2. Green Door")
        print("3. Blue Door")
        
        choice = input("\nEnter your choice: ")

        if choice == "1":
            print("\nYou entered the Red Door and faced a dangerous dragon. GAME OVER!")
            break
        elif choice == "2":
            print("\nThe Green Door led you to a beautiful garden. YOU WON!")
            break
        elif choice == "3":
            print("\nYou entered the Blue Door and found a friendly monster. You became friends and continued on your journey together. YOU WON!")
            break
        else:
            print("\nInvalid choice! Please choose a valid door number to continue.")

if __name__ == "__main__":
    start_game()