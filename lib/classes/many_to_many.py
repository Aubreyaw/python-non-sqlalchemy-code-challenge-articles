class Article:
    # List of all articles
    all = []
    
    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine

        # Validate and set article title 
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if len(title) < 5 or len(title) > 50:
            raise ValueError("Title must have between 5 and 50 characters")
        self._title = title
        Article.all.append(self)

    @property
    def title(self):
        # Read-only property, article title cannot be updated
        return self._title
    
    @property
    def author(self):
        # Property allows updating the article's associated Author object via setter
        return self._author
    
    @author.setter
    def author(self, value):
        # Update and validate author object
        if not isinstance(value, Author):
            raise TypeError("Author must be an instance of the Author class")
        self._author = value

    @property
    def magazine(self):
        # Property allows updating the article's associated Magazine object via setter
        return self._magazine
    
    @magazine.setter
    def magazine(self, value):
        # Update and validate magazine object
        if not isinstance(value, Magazine):
            raise TypeError("Magazine must be an instance of the Magazine class")
        self._magazine = value


# Author 
class Author:
    def __init__(self, name):
        # Validate and set author's name
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if len(name) == 0:
            raise ValueError("Name must have more than 0 characters")
        self._name = name
    
    @property
    def name(self):
        # Read-only property, author's name cannot be updated
         return self._name
        
    def articles(self):
        # Returns a list of all of the articles written by that author
        return [article for article in Article.all if article.author == self]
    
    def magazines(self):
        # Returns a list of magazines that author has articles in 
        return list(set(article.magazine for article in self.articles()))

    def add_article(self, magazine, title):
        # Creates and returns a new Article instance for the author
        return Article(self, magazine, title)

    def topic_areas(self):
        # Returns a unique list of magazine categories that author has contributed to
        if not self.articles():
            return None
        return list(set(article.magazine.category for article in self.articles())) 


# Magazine
class Magazine:
    def _validate_name(self, name):
        # Validate magazine name
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if len(name) < 2 or len(name) > 16:
            raise ValueError("Name must be between 2 and 16 characters") 
    
    def _validate_category(self, category):
        # Validate category name
        if not isinstance(category, str):
            raise TypeError("Category must be a string")
        if len(category) == 0:
            raise ValueError("Category must be between more than 0 characters")

    def __init__(self, name, category):
        # Validate and set the magazine's name
        self._validate_name(name)
        self._name = name
        # Validate and set the magazine's category
        self._validate_category(category)
        self._category = category

    @property
    def name(self):
        # Property for magazine name, can be updated via setter
        return self._name   

    @name.setter
    def name(self, new_name):
        # Validate and update magazine name
        self._validate_name(new_name)
        self._name = new_name

    @property
    def category(self):
        # Property for magazine category, can be updated via setter
        return self._category

    @category.setter
    def category(self, new_category):
        # Validate and update magazine category
        self._validate_category(new_category)
        self._category = new_category

    def articles(self):
        # Returns that magazine's articles
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        # Returns a list of authors that have contributed to that magazine
        return list(set(article.author for article in self.articles()))

    def article_titles(self):
        # Returns titles of articles for that magazine
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        # Returns a list of authors who have written more than 2 articles for the magazine
        author_counts = {}
        for article in self.articles():
            author = article.author
            author_counts[author] = author_counts.get(author, 0) + 1
        result = [author for author, count in author_counts.items() if count > 2]
        return result if result else None

    @classmethod
    # Returns a dictionary mapping each magazine to its article count 
    def magazine_article_counts(cls):
        counts = {}
        for article in Article.all:
            mag = article.magazine
            counts[mag] = counts.get(mag, 0) + 1
        return counts

    @classmethod
    # Returns the magazine with the most articles published
    def top_publisher(cls):
        counts = cls.magazine_article_counts()
        return max(counts, key=counts.get) if counts else None