# gram-graph

[See a live demo here](https://gram-graph.herokuapp.com/)

_work in progress_

A data analysis and visualisation application that represents a network of Instagram followers as a directed graph with nodes and edges in order to identify central accounts in a neighbourhood around a stipulated account.

## Project description

### Social networks as nodes and edges

Social networks lend themselves to graph analysis ([graphs](https://en.wikipedia.org/wiki/Graph_theory) in the mathematical sense, not charts). The nodes are the accounts, and the edges are the connections between those accounts. How you represent these connections depends on the structure of that social network. On Facebook, a friend is a bidirectional relationship, so that could be represented as an undirected graph. However, on Twitter, followers are not bidirectional. I can follow Elon Musk without him following me and so these types of social networks are best understood as a directed graph. Once represented as a graph with nodes and edges, you can apply standard tools from graph theory. The aim is to try and identify central or important accounts in a neighbourhood of accounts.

### Analysing an Instagram neighbourhood

This project attempts to analyse connections between Instagram followers, in the neighbourhood surrounding a specified account. `networkx` is used to represent the network of followers as a directed graph. Followers data is scraped using `InstaPy` and stored in a `sqlite` database. The data is then represented as a `plotly` chart and saved as a JSON file. That JSON file is used in a simple one page `flask` application that visualises the network (pruning nodes with few connections) and also reports back summary data about the most central accounts. It is currently hosted on Heroku.

### Intended improvements

This project is still a work in progress, and there are many issues which need to be improved on.

Currently the only centrality measure is degree centrality, which is just a fancy term for the number of followers each account has. It is the simplest measure of centrality. But degree centrality fails to extract more subtle notions of centrality. The accounts with the most followers are not necessarily the accounts that are most important in terms of connecting the overall network. The intention is to expand this analysis by including more rigorous measures of centrality such as betweenness centrality and closeness centrality.

In addition, the application is not yet general purpose. It is currently being tested on a single account: [happyhoundsza](https://instagram.com/happyhoundsza), a organic dog food company in Cape Town. Eventually this application should allow anyone to input their username and see the graph of accounts in their vicinity. However, there are a few obstacles to this:

- The data fetching process is _slow_. Because there is no follower API for instagram (or at least an accessible one), `InstaPy` must scrape the website for followers details. This is extremely time consuming. For an account with 2000 followers, and a depth of 2 (i.e. get that account's followers, and the followers of the account's followers), it can take on the order of magnitude of a few days. `InstaPy` is also tricky to configure.
- In addition, Instagram considers any form of web scraping to go against its code of conduct, and so `InstaPy` has to regulate its queries, taking breaks when appropriate.

This means that the ideal of inputting your username and immediately seeing the graph visualised on the page is impossible. A more likely approach would be for users to submit requests on the site, and then get notified at a later stage when their graph is ready for viewing.

All these factors together suggest that the applications of this project are limited. The main purpose for myself was educational. I have just finished working through [Data Science from Scratch](https://www.oreilly.com/library/view/data-science-from/9781492041122/), and wanted to apply some of the concepts from there.

## Local Usage

### Install dependencies and configure

First, clone the repository, create a virtual environment and install the requirements (what follows a `$` should be typed into a command prompt).

```console
$ git clone https://github.com/emilioziniades/gram-graph
$ cd gram-graph
$ python -m venv venv
$ source /venv/bin/activate
$ pip install -r requirements.txt
```

You will need to configure some environment variables. The easiest way to do this is to create a file named `.env` in the project's root directory, and add the following, replacing `yourusername` and `yourpassword`

```
INSTAGRAM_USERNAME=yourusername
INSTAGRAM_PASSWORD=yourpassword
FLASK_ENV=development
```

To see the application in action, simply run the following and visit the link provided in the browser.

```console
$ export FLASK_APP=gramgraph
$ flask run
```

### Collect and prepare data

Initially, the application will show the existing database for Happy Hounds. If you want to collect fresh data for a different account, do the following.

1. Delete the `data` folder.
2. Go to `/app/config.py` and change the value of the `ACCOUNT` variable.
3. Run `flask collect` in a terminal. This will collect all the data from instagram and store it in a local db. Be prepared to wait.
4. Next, run `flask prepare` in a terminal. It will process all the data, extract the summary and save all the information in JSON.
5. Run `flask run` again, and you should be able to see the new graph in a browser. Enjoy!

## Contributing

Contributions are always welcome! Please open a new issue if you find a bug, or create a pull request with a new feature you think is cool.
