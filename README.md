# Automated Python Crawler

About:

    This automated python crawler extracts datas from the brazilian National Water Agency, such as: 
        The agency authority name.
        The authority agent name and occupation
        and some of his appointments agenda data.

    There is a wizard in the code that will help you.

Instructions:

    To run this code you can add this folder, whitin all it's content, and debug from your code editor,
    or,
    as this crawler is containerized in docker, you can also run there. 
    
    This code returns 2 .json files:
        The first one is a dictionary that contains the previously required data.
        The other one is the data organized per lists.


Commands: 

    docker build -t python-crawler .   (Command to build a docker image)
    docker run -t -i python-crawler    (Command to run the docker image created)      