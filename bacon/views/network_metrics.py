from django.http import HttpResponse
from rest_framework.decorators import api_view
from neo4jrestclient.client import GraphDatabase, Node, Relationship
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from urlparse import urlparse, urlunparse

@csrf_exempt
@api_view(["GET"])
def shortest_path(request):
    name_one = request.GET.get("name_one")
    name_two = request.GET.get("name_two")
    if name_one is None and name_two is None:
        response_json = json.dumps({
            'status': 1,
            'data': "Invalid Data",
            'instance_name': settings.INSTANCE_NAME,
            'count': 0
        })
        return HttpResponse(response_json, content_type="application/json", status=400)
    url = urlparse(settings.GRAPHENEDB_URL)
    url_without_auth = urlunparse((url.scheme, "{0}:{1}".format(url.hostname, url.port), url.path, None, None, None))

    graph = GraphDatabase(url_without_auth, username = url.username, password = url.password)
    # graph = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="1123581321")
    q = """
        MATCH p=shortestPath((bacon:Actor {{name:"{name_one}"}})-[*]-(meg:Actor {{name:"{name_two}"}}))
        RETURN p
        """
    result = graph.query(q=q.format(name_one=name_one, name_two=name_two), data_contents=True)
    response_json = json.dumps({
            'status': 1,
            'data': result.graph[0],
            'instance_name': settings.INSTANCE_NAME,
            'count': 0
        })
    # Hardcoding For Frontend dev
    # response_json = json.dumps({"status": 1, "instance_name": "local", "data": {"relationships": [{"endNode": "686", "startNode": "696", "type": "Acted_In", "id": "100848", "properties": {}}, {"endNode": "4888", "startNode": "2249", "type": "Acted_In", "id": "9843", "properties": {}}, {"endNode": "4888", "startNode": "696", "type": "Acted_In", "id": "9844", "properties": {}}, {"endNode": "686", "startNode": "690", "type": "Acted_In", "id": "873", "properties": {}}], "nodes": [{"labels": ["Actor"], "id": "690", "properties": {"name": "Aishwarya Rai"}}, {"labels": ["Actor"], "id": "696", "properties": {"name": "Satish Kaushik"}}, {"labels": ["Movie"], "id": "4888", "properties": {"name": "Road, Movie"}}, {"labels": ["Actor"], "id": "2249", "properties": {"name": "Abhay Deol"}}, {"labels": ["Movie"], "id": "686", "properties": {"name": "Aa Ab Laut Chalen"}}]}, "count": 0})
    return HttpResponse(response_json, content_type="application/json")


@csrf_exempt
@api_view(["GET"])
def degree_centrality(request):
    name_one = request.GET.get("name_one")
    graph = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="1123581321")
    q = """
        MATCH (ab:Actor {{name:"{name_one}"}})-[:Acted_In]->(m)<-[:Acted_In]-(coActors)
        RETURN Distinct(coActors.name), m.name
        """
    result = graph.query(q=q.format(name_one=name_one), data_contents=True)
    response_json = json.dumps({
            'status': 1,
            'data': list(result),
            'instance_name': settings.INSTANCE_NAME,
            'count': 0
        })
    # Hardcoding For Frontend dev
    response_json = json.dumps({"status": 1, "instance_name": "local", "data": [["Saurabh Shukla", "Taal"], ["Mita Vashist", "Taal"], ["Sushma Seth", "Taal"], ["Amrish Puri", "Taal"], ["Alok Nath", "Taal"], ["Akshay Khanna", "Taal"], ["Anil Kapoor", "Taal"], ["Aishwarya Rai-Bachchan", "Taal"], ["Akshaye Khanna", "Taal"], ["Karishma Kapoor", "Shakti - The Power"], ["Sanjay Kapoor", "Shakti - The Power"], ["Nana Patekar", "Shakti - The Power"], ["Shahrukh Khan", "Shakti - The Power"], ["Moushmi Chatterjee", "Aa Ab Laut Chalen"], ["Alok Nath", "Aa Ab Laut Chalen"], ["Himani Shivpuri", "Aa Ab Laut Chalen"], ["Viveck Vaswani", "Aa Ab Laut Chalen"], ["Jaspal Bhatti", "Aa Ab Laut Chalen"], ["Satish Kaushik", "Aa Ab Laut Chalen"], ["Paresh Rawal", "Aa Ab Laut Chalen"], ["Kader Khan", "Aa Ab Laut Chalen"], ["Navin Nischol", "Aa Ab Laut Chalen"], ["Suman Ranganathan", "Aa Ab Laut Chalen"], ["Aishwarya Rai", "Aa Ab Laut Chalen"], ["Akshay Khanna", "Aa Ab Laut Chalen"], ["Rajesh Khanna", "Aa Ab Laut Chalen"], ["Aishwarya Rai-Bachchan", "Aa Ab Laut Chalen"], ["Akshaye Khanna", "Aa Ab Laut Chalen"], ["Sonali Bendre", "Dhaai Akshar Prem Ke"], ["Salman Khan", "Dhaai Akshar Prem Ke"], ["Inder Sudan", "Dhaai Akshar Prem Ke"], ["Supriya Karnik", "Dhaai Akshar Prem Ke"], ["Himani Shivpuri", "Dhaai Akshar Prem Ke"], ["Tanvi Azmi", "Dhaai Akshar Prem Ke"], ["Neena Kulkarni", "Dhaai Akshar Prem Ke"], ["Dilip Tahil", "Dhaai Akshar Prem Ke"], ["Harish Patel", "Dhaai Akshar Prem Ke"], ["Sushma Seth", "Dhaai Akshar Prem Ke"], ["Shakti Kapoor", "Dhaai Akshar Prem Ke"], ["Anupam Kher", "Dhaai Akshar Prem Ke"], ["Amrish Puri", "Dhaai Akshar Prem Ke"], ["Aishwarya Rai", "Dhaai Akshar Prem Ke"], ["Abhishek Bachchan", "Dhaai Akshar Prem Ke"], ["Rana Jung Bahadur", "Hamara Dil Aapke Paas Hai"], ["Upasna Singh", "Hamara Dil Aapke Paas Hai"], ["Himani Shivpuri", "Hamara Dil Aapke Paas Hai"], ["Razzak Khan", "Hamara Dil Aapke Paas Hai"], ["Jaspal Bhatti", "Hamara Dil Aapke Paas Hai"], ["Johny Lever", "Hamara Dil Aapke Paas Hai"], ["Anupam Kher", "Hamara Dil Aapke Paas Hai"], ["Anang Desai", "Hamara Dil Aapke Paas Hai"], ["Mukesh Rishi", "Hamara Dil Aapke Paas Hai"], ["PURU RAJKUMAR", "Hamara Dil Aapke Paas Hai"], ["Sonali Bendre", "Hamara Dil Aapke Paas Hai"], ["Aishwarya Rai", "Hamara Dil Aapke Paas Hai"], ["Anil Kapoor", "Hamara Dil Aapke Paas Hai"], ["Aishwarya Rai-Bachchan", "Hamara Dil Aapke Paas Hai"], ["Shakti Kapoor", "Josh"], ["SHEETAL", "Josh"], ["Raj Kiran", "Josh"], ["Deven Verma", "Josh"], ["Vidya Sinha", "Josh"], ["Amjad Khan", "Josh"], ["Nitin Raikwar</br></br></br></font>", "Josh"], ["<font color=\"#000000\">Producer: Venus Records &amp; TapesDirector: Mansoor KhanMusic: Anu MalikLyrics: Sameer", "Josh"], ["KAPOOR", "Josh"], ["SHAKTI", "Josh"], ["<strong></br></strong>", "Josh"], ["Shah Rukh Khan", "Josh"], ["Aishwarya Rai-Bachchan", "Josh"], ["Chandrachur Singh", "Josh"], ["Shahrukh Khan", "Josh"], ["Priya Gill", "Josh"], ["Sharad Kapoor", "Josh"], ["RAMMOHAN", "Mela"], ["Rajendra Nath", "Mela"], ["Lalita Pawar", "Mela"], ["RANDHIR", "Mela"], ["Feroz Khan", "Mela"], ["Mumtaz", "Mela"], ["Sanjay Khan", "Mela"], ["Aamir Khan", "Mela"], ["Twinkle Khanna", "Mela"], ["Faisal Khan", "Mela"], ["Johny Lever", "Mela"], ["Dilip Kumar", "Mela"], ["Nargis", "Mela"], ["Jeevan", "Mela"], ["ROOPKAMAL", "Mela"], ["Amar", "Mela"], ["Rehman", "Mela"], ["Zubaida", "Mela"], ["Produced By: WADIA FILMS", "Mela"], ["Firoz Khan", "Mela"], ["RAJENDRA", "Mela"], ["NATH", "Mela"], ["Ram Mohan", "Mela"], ["Cast:: Aamir Khan", "Mela"], ["Producer: Dharmesh Darshan", "Mela"], ["Shefali Chhaya", "Mohabbatein"], ["Amrish Puri", "Mohabbatein"], ["Aishwarya Rai", "Mohabbatein"], ["Preeti Jhangiani", "Mohabbatein"], ["Jimmy Shergill", "Mohabbatein"], ["Kim Sharma", "Mohabbatein"], ["Jugal Hansraj", "Mohabbatein"], ["Shamita Shetty", "Mohabbatein"], ["Uday Chopra", "Mohabbatein"], ["Shahrukh Khan", "Mohabbatein"], ["Amitabh Bachchan", "Mohabbatein"], ["Aishwarya Rai-Bachchan", "Mohabbatein"], ["Shah Rukh Khan", "Mohabbatein"], ["Prem Chopra", "Sanam Tere Hain Hum"], ["Kiran Kumar", "Sanam Tere Hain Hum"], ["Kulbhushan Kharbanda", "Sanam Tere Hain Hum"], ["Upasna Singh", "Sanam Tere Hain Hum"], ["Amita Nangia", "Sanam Tere Hain Hum"], ["Sunil Diwan", "Sanam Tere Hain Hum"], ["Anjala Zaveri", "Sanam Tere Hain Hum"], ["Kirti Reddy", "Sanam Tere Hain Hum"], ["Nagarjuna Akkineni", "Sanam Tere Hain Hum"], ["Zayed Khan", "Shabd"], ["Sanjay Dutt", "Shabd"], ["Rimi Sen", "Dhoom 2"], ["Uday Chopra", "Dhoom 2"], ["Bipasha Basu", "Dhoom 2"], ["Hrithik Roshan", "Dhoom 2"], ["Abhishek Bachchan", "Dhoom 2"], ["Yusuf Hussain", "Dhoom 2"], ["Deena Pathak", "Umrao Jaan"], ["Prema Narayan", "Umrao Jaan"], ["Raj Babbar", "Umrao Jaan"], ["Naseeruddin Shah", "Umrao Jaan"], ["Farooq Sheikh", "Umrao Jaan"], ["Rekha", "Umrao Jaan"], ["Farooq Shaikh", "Umrao Jaan"], ["Shabana Azmi", "Umrao Jaan"], ["Aishwarya Rai-Bachchan", "Umrao Jaan"], ["Abhishek Bachchan", "Umrao Jaan"], ["Divya Dutta", "Umrao Jaan"], ["Sunil Shetty", "Umrao Jaan"], ["Gulshan Grover", "Raavan"], ["Om Puri", "Raavan"], ["Smita Patil", "Raavan"], ["Vikram", "Raavan"], ["Nikhil Dwivedi", "Raavan"], ["Govinda", "Raavan"], ["Abhishek Bachchan", "Raavan"], ["Aishwarya Rai-Bachchan", "Raavan"], ["Danny Denzongpa", "Robot"], ["Rajinikanth", "Robot"], ["Aishwarya Rai-Bachchan", "Robot"], ["Randhir Kapoor", "Action Replayy"], ["Neha Dhupia", "Action Replayy"], ["Akshay Kumar", "Action Replayy"], ["Aishwarya Rai-Bachchan", "Action Replayy"], ["Hrithik Roshan", "Guzaarish"], ["Aditya Roy Kapur", "Guzaarish"], ["Aishwarya Rai-Bachchan", "Guzaarish"], ["Saeed Jaffrey", "Albela"], ["Jackie Shroff", "Albela"], ["Namrata Shirodkar", "Albela"], ["Aishwarya Rai", "Albela"], ["Govinda", "Albela"], ["Beena", "Aur Pyar Ho Gaya"], ["Shammi Kapoor", "Aur Pyar Ho Gaya"], ["Anupam Kher", "Aur Pyar Ho Gaya"], ["Aishwarya Rai", "Aur Pyar Ho Gaya"], ["Bobby Deol", "Aur Pyar Ho Gaya"], ["Rajeev Verma", "Hum Dil De Chuke Sanam"], ["Kenny Desai", "Hum Dil De Chuke Sanam"], ["Rekho Rao", "Hum Dil De Chuke Sanam"], ["Smita Jayakar", "Hum Dil De Chuke Sanam"], ["Vikram Gokhale", "Hum Dil De Chuke Sanam"], ["Zohra Sehgal", "Hum Dil De Chuke Sanam"], ["Aishwarya Rai", "Hum Dil De Chuke Sanam"], ["Ajay Devgan", "Hum Dil De Chuke Sanam"], ["Salman Khan", "Hum Dil De Chuke Sanam"], ["Producer &amp; Director : Sanjay Leela Bhansali", "Hum Dil De Chuke Sanam"], ["Ajay Devgn", "Hum Dil De Chuke Sanam"], ["Aishwarya Rai-Bachchan", "Hum Dil De Chuke Sanam"], ["Aslam", "Dil Ka Rishta"], ["Jill", "Dil Ka Rishta"], ["Linda", "Dil Ka Rishta"], ["Willy", "Dil Ka Rishta"], ["Priyanshu Chatterjee", "Dil Ka Rishta"], ["Goolshan Mazdasani", "Dil Ka Rishta"], ["Pankaj Berry", "Dil Ka Rishta"], ["Rajesh Vivek", "Dil Ka Rishta"], ["Master Hitanshu Lodhiya", "Dil Ka Rishta"], ["Tinu Talsania", "Dil Ka Rishta"], ["Paresh Rawal", "Dil Ka Rishta"], ["Isha Koppikar", "Dil Ka Rishta"], ["Arjun Rampal", "Dil Ka Rishta"], ["Aishwarya Rai", "Dil Ka Rishta"], ["Rakhee", "Dil Ka Rishta"], ["Paresh Rawal", "Hum Kisi Se Kum Nahin"], ["Annu Kapoor", "Hum Kisi Se Kum Nahin"], ["Satish Kaushik", "Hum Kisi Se Kum Nahin"], ["Aishwarya Rai", "Hum Kisi Se Kum Nahin"], ["Rishi Kapoor", "Hum Kisi Se Kum Nahin"], ["Amjad Khan", "Hum Kisi Se Kum Nahin"], ["Kajal Kiran", "Hum Kisi Se Kum Nahin"], ["Tariq", "Hum Kisi Se Kum Nahin"], ["Agha", "Hum Kisi Se Kum Nahin"], ["Kamal Kapoor", "Hum Kisi Se Kum Nahin"], ["", "Hum Kisi Se Kum Nahin"], ["Om Shivpuri", "Hum Kisi Se Kum Nahin"], ["Amitabh Bachchan", "Hum Kisi Se Kum Nahin"], ["Sanjay Dutt", "Hum Kisi Se Kum Nahin"], ["Ajay Devgan", "Hum Kisi Se Kum Nahin"], ["Aishwarya Rai", "Hum Tumhare Hain Sanam"], ["Salman Khan", "Hum Tumhare Hain Sanam"], ["Madhuri Dixit", "Hum Tumhare Hain Sanam"], ["Shahrukh Khan", "Hum Tumhare Hain Sanam"], ["Lakshmi", "Jeans"], ["Raju Sundaram", "Jeans"], ["Senthil", "Jeans"], ["Prashant Nasser", "Jeans"], ["Aishwarya Rai", "Jeans"]], "count": 0})
    return HttpResponse(response_json, content_type="application/json")


@csrf_exempt
@api_view(["GET"])
def actors_of_a_movie(request):
    name_one = request.GET.get("name_one")
    graph = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="1123581321")
    q = """
        MATCH (p:Actor)-[:Acted_In]->(m:Movie)
        WHERE m.name=~"(?i){name_one}"
        RETURN Distinct(p.name)
        """
    result = graph.query(q=q.format(name_one=name_one), data_contents=True)
    response_json = json.dumps({
            'status': 1,
            'data': list(result),
            'instance_name': settings.INSTANCE_NAME,
            'count': 0
        })
    # Hardcoding For Frontend dev
    response_json = json.dumps({"status": 1, "instance_name": "local", "data": [["Pran"], ["Mohan Choti"], ["Ulhas"], ["Agha"], ["Simmi"], ["Manoj Kumar"], ["Waheeda Rehman"], ["Dilip Kumar"]], "count": 0})
    return HttpResponse(response_json, content_type="application/json")
