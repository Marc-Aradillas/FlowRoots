import sys
from modules import learn, discover, contribute
from chatbot import bot

def main_menu():
    while True:
        print("\n================================")
        print("   Welcome to the FlowRoots App")
        print("================================")
        print("Please choose an option:")
        print("1. Learn about styles or history")
        print("2. Discover events, crews, or music")
        print("3. Contribute or share content")
        print("4. Chat with the AI Assistant")
        print("5. Exit")
        
        choice = input("> ").strip()
        
        if choice == "1":
            learn.menu()
        elif choice == "2":
            discover.menu()
        elif choice == "3":
            contribute.menu()
        elif choice == "4":
            bot.chat()
        elif choice == "5":
            print("Thanks for using FlowRoots! Goodbye 👋")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()