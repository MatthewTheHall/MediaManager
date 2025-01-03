class MediaEntry:
    def __init__(self, mediaType, name, year, genre, rating):
        #Storing entry details in attributes
        self.mediaType = mediaType
        self.name = name
        self.year = year
        self.genre = genre
        self.rating = rating

    def __str__(self):
        #changing the entry details into a readable string format
        return "{} ({}) - {} | Genre: {} | Rating: {}".format(
            self.name, self.year, self.mediaType, self.genre, self.rating
        )


class Validator:
    @staticmethod  #necessary because the method doesn't use self. Prevents Python from expecting a self argument.
    def validateInteger(value, minValue=None, maxValue=None, length=None):
        #this is to ensure input is an integer and meets specified criteria (min, max, length)
        try:
            value = int(value)  #convert input to integer
            if minValue is not None and value < minValue:  #check minimum value
                raise ValueError("Value is below the minimum allowed.")
            if maxValue is not None and value > maxValue:  #check maximum value
                raise ValueError("Value exceeds the maximum allowed.")
            if length is not None and len(str(value)) != length:  #check length
                raise ValueError("Value does not have the required number of digits.")
            return value
        except ValueError as e:
            raise e  #pass error to the calling function instead of handling it within this method

    @staticmethod
    def validateChoice(value, choices):
        #this is to ensure input is a valid choice
        try:
            value = int(value)  #convert input to integer
            if value not in choices:  #check if value is in the allowed list
                raise ValueError("Invalid choice. Please select from {}".format(choices))
            return value 
        except ValueError as e:
            raise e  #passing error to the function calling this


class DataManager:
    def __init__(self, filePath):
        #set file path for saving and loading data
        self.filePath = filePath

    def loadData(self):
        #load entries from file
        entries = []
        try:
            with open(self.filePath, "r", encoding="utf-8") as f:  #open file for reading
                for line in f:
                    line = line.strip()  #remove whitespace
                    if line:  #skip empty lines
                        parts = line.split("|")  #split line into parts (type|name|year|genre|rating)
                        if len(parts) == 5:  #ensure line has correct format
                            entry = MediaEntry(
                                mediaType=parts[0],
                                name=parts[1],
                                year=parts[2],
                                genre=parts[3],
                                rating=parts[4],
                            )
                            entries.append(entry)  #add entry to list at the bottom rather than replacing it all
        except FileNotFoundError:
            print("No existing data found.")  #handle missing file
        return entries  #return list of entries

    def saveData(self, entries):
        #save entries to the file
        with open(self.filePath, "w", encoding="utf-8") as f:  #open file for writing
            for entry in entries:
                f.write("|".join([entry.mediaType, entry.name, entry.year, entry.genre, entry.rating]) + "\n")  #write each entry


class MediaManager:
    def __init__(self):
        #initialize data manager and entry list
        self.dataManager = DataManager("medialog.txt") #the file medialog.txt being created for storing data
        self.entries = []

    def initialize(self):
        #load data from file into entries
        self.entries = self.dataManager.loadData()

    def addEntry(self):
        #add a new entry
        print("Choose type:")
        print("1. TV Show")
        print("2. Movie")
        typeChoice = None
        while typeChoice is None:  #keep asking until a valid choice
            try:
                typeChoice = Validator.validateChoice(input("Enter 1 or 2: "), [1, 2])
            except ValueError as e:
                print(str(e))
        mediaType = "TV Show" if typeChoice == 1 else "Movie"  #set media type to TV Show or Movie (1 or 2)

        name = input("Enter name: ").strip()  #requesting name
        year = None
        while year is None:  
            try: #keep asking until a valid year is added
                year = Validator.validateInteger(input("Enter year: "), length=4) #making the valid year require 4 digits
            except ValueError as e:
                print(str(e))
        genre = input("Enter genre: ").strip()  #requesting genre
        rating = None
        while rating is None: 
            try: #this is making you choose a valid rating 0-10
                rating = Validator.validateInteger(input("Enter rating (0-10): "), minValue=0, maxValue=10)
            except ValueError as e:
                print(str(e))

        for entry in self.entries:  #checks for duplicate entries
            if entry.name == name and entry.year == str(year): #same name and year check
                print("Entry already exists! Choose action:")
                action = input("'update rating', 'add another', or 'cancel': ").strip().lower()
                if action == "update rating":  #updates rating if chosen
                    entry.rating = str(rating)
                    print("Rating updated.")
                elif action == "add another": #add another entry if chosen
                    self.addEntry()
                return

        newEntry = MediaEntry(
            mediaType=mediaType, name=name, year=str(year), genre=genre, rating=str(rating)
        )
        self.entries.append(newEntry)  #add the new entry to the list at the bottom
        print("New entry added successfully!")

    def searchEntry(self):
        #search for entries or report if invalid
        searchOption = input("Search by: 'name', 'genre', or 'rating': ").strip().lower() #choose to search by name, genre, or rating
        if searchOption == "name":
            searchName = input("Enter name to search: ").strip()
            foundEntries = [entry for entry in self.entries if entry.name.lower() == searchName.lower()]  #search by name
        elif searchOption == "genre":
            searchGenre = input("Enter genre to search: ").strip()
            foundEntries = [entry for entry in self.entries if entry.genre.lower() == searchGenre.lower()]  #search by genre
        elif searchOption == "rating":
            searchRating = None
            while searchRating is None:  #keep asking until a valid rating is entered 0-10
                try:
                    searchRating = Validator.validateInteger(input("Enter rating to search (0-10): "), minValue=0, maxValue=10)
                except ValueError as e:
                    print(str(e))
            foundEntries = [entry for entry in self.entries if entry.rating == str(searchRating)]  #search by rating
        else:
            print("Invalid search option.") 
            return

        if foundEntries:  #prints found entries or tells you if none found
            for entry in foundEntries:
                print(entry)
        else:
            print("No entries found.") 

    def viewStatistics(self):
        #view statistics of entries
        if not self.entries:
            print("No data available.") 
            return
        ratings = [float(entry.rating) for entry in self.entries if entry.rating.isdigit()]  #collect valid ratings
        if not ratings:
            print("No valid ratings in the data.")
            return
        print("Overall Statistics:")
        print("Count: {}".format(len(self.entries)))  #show total count of media
        print("Average Rating: {:.2f}".format(sum(ratings) / len(ratings)))  #show average rating
        highestRated = max(self.entries, key=lambda x: float(x.rating))  #find highest rated
        lowestRated = min(self.entries, key=lambda x: float(x.rating))  #find lowest rated
        print("Highest Rated: {} ({})".format(highestRated.name, highestRated.rating))
        print("Lowest Rated: {} ({})".format(lowestRated.name, lowestRated.rating))

    def run(self):
        #this is the main menu loop for choosing to add entry, search entry, view stats, or exit and save data
        self.initialize()  #load data
        while True:
            print("\nMenu: add entry, search entry, view stats, exit")
            choice = input("Enter choice: ").strip().lower()
            if choice == "add entry":
                self.addEntry()  
            elif choice == "search entry":
                self.searchEntry()  
            elif choice == "view stats":
                self.viewStatistics() 
            elif choice == "exit":
                self.dataManager.saveData(self.entries)  #save data and exit
                print("Data saved. Exiting program.")
                break
            else:
                print("Invalid option. Please try again.") 


if __name__ == "__main__":   #added this in case this is imported as a module and doesn't auto run.
    mediamanager = MediaManager()  #creating manager instance
    mediamanager.run()  #run the program






