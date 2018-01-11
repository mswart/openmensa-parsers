from .parser import parse_url


def test_parse_url():
    result = parse_url(
        'https://web.archive.org/web/20171204101926/'
        + 'http://www.studierendenwerk-aachen.de/speiseplaene/academica-w.html'
    )

    assert result == expected_result


expected_result = """<?xml version="1.0" encoding="UTF-8"?>
<openmensa version="2.1" xmlns="http://openmensa.org/open-mensa-v2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd">
  <canteen>
    <day date="2017-12-04">
      <category name="Tellergericht">
        <meal>
          <name>Linseneintopf | Speck | Bockwurst | Brötchen</name>
          <note>Antioxidationsmittel</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Phosphat</note>
          <note>Sellerie</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">3.30</price>
          <price role="student">1.80</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Chili sin Carne | Kräuterreis</name>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">3.60</price>
          <price role="student">2.10</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Lammcurry mit Joghurt | Reis</name>
          <note>Milch</note>
          <price role="other">5.40</price>
          <price role="student">3.90</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Hähnchen Döner-Art | Joghurtdip</name>
          <note>Milch</note>
          <note>Sojabohnen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Gamberetti | Shrimps, Spinat, Knoblauch, Oliven</name>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Krebstiere</note>
          <note>Milch</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <note>geschwärzt</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Express">
        <meal>
          <name>Hähnchen Döner-Art | Joghurtdip | Pommes frites | Fingermöhrchen</name>
          <note>Milch</note>
          <note>Sojabohnen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Conchiglie al forno | Gemüse | Rinderhack | Béchamel</name>
          <note>Eier</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Gnocchi al forno | Brokkoli, Kochschinken, Käse | Béchamel</name>
          <note>Antioxidationsmittel</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Phosphat</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Gnocchi Mediterranea | Champignons, Spinat | Béchamel</name>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Tortiglioni Poletto | Geflügel, Paprikasauce, Rucola</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Schweinefleisch Woyishau | Aprikosen, Pflaumen | Basmatireis</name>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
        <meal>
          <name>Gemüse-Wok Woyishau | Basmatireis</name>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
      </category>
      <category name="Burger Classics mit Pommes und Softgetränk">
        <meal>
          <name>Hamburger | Pommes | Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Cheeseburger | Pommes | Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Chicken Burger | Pommes | Getränk 0,25 L</name>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Veggieburger | Pommes | Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
      </category>
      <category name="Burger des Tages mit Pommes und Softgetränk">
        <meal>
          <name>Gorgonzola-Bacon-Burger | Laugenbrötchen, Preiselbeeren, Rucola</name>
          <note>Antioxidationsmittel</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">6.90</price>
          <price role="student">5.40</price>
        </meal>
      </category>
      <category name="Fingerfood mit Pommes und Softgetränk">
        <meal>
          <name>Chicken Wings 6 Stück mit einem Dip | Pommes | Getränk 0,25 L</name>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Hähnchennuggets 9 Stück mit 2 Dips | Pommes | Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Sandwich mit Softgetränk">
        <meal>
          <name>Elsässer Art | Zwiebeln, Crème Fraîche, Speck | Käse</name>
          <note>Antioxidationsmittel</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Hafer</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Roggen</note>
          <note>Sesamsamen</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Spießbraten | Schmorzwiebeln | Lyoner Kartoffeln</name>
          <price role="other">6.00</price>
          <price role="student">4.50</price>
        </meal>
      </category>
      <category name="Hauptbeilagen">
        <meal>
          <name>Pommes Frites oder Reis</name>
        </meal>
      </category>
      <category name="Nebenbeilage">
        <meal>
          <name>Fingermöhrchen</name>
        </meal>
      </category>
    </day>
    <day date="2017-12-05">
      <category name="Tellergericht">
        <meal>
          <name>Feuriger Curry Gemüseeintopf | Putenstreifen | Vollkornreis</name>
          <note>Erdnüsse</note>
          <note>Gluten</note>
          <note>Senf</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">3.30</price>
          <price role="student">1.80</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Indisches Karottencurry</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <price role="other">3.60</price>
          <price role="student">2.10</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Putenscaloppine | Zitronensauce</name>
          <note>Milch</note>
          <price role="other">5.40</price>
          <price role="student">3.90</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Schweineschnitzel | Jalapeño-Käsesauce</name>
          <note>Eier</note>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Erbaccie | Gorgonzola, Broccoli, Spinat</name>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Express">
        <meal>
          <name>Schweineschnitzel | Jalapeño-Käsesauce | Pommes frites | Kaisergemüse</name>
          <note>Eier</note>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Lachslasagne | Rahmspinat | Tomatensauce</name>
          <note>Eier</note>
          <note>Farbstoff</note>
          <note>Fische</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Spaghetti al Arrabiata | Tomaten-Chili-Sauce</name>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Weizen</note>
          <note>geschwärzt</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Conchiglie Funghi e Carne | Pilze, Schweinefleisch | Bechamelsauce | Bratensauce</name>
          <note>Eier</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Thai Red Curry | Gemüse, Putenstreifen | Korianderreis</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
        <meal>
          <name>Rotes Thai Curry mit Gemüse | Korianderreis</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
      </category>
      <category name="Burger Classics mit Pommes und Softgetränk">
        <meal>
          <name>Hamburger | Pommes | Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Cheeseburger | Pommes | Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Chicken Burger | Pommes | Getränk 0,25 L</name>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Veggieburger | Pommes | Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
      </category>
      <category name="Burger des Tages mit Pommes und Softgetränk">
        <meal>
          <name>Gorgonzola-Bacon-Burger | Laugenbrötchen, Preiselbeeren, Rucola</name>
          <note>Antioxidationsmittel</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">6.90</price>
          <price role="student">5.40</price>
        </meal>
      </category>
      <category name="Fingerfood mit Pommes und Softgetränk">
        <meal>
          <name>Chicken Wings 6 Stück mit einem Dip | Pommes | Getränk 0,25 L</name>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Hähnchennuggets 9 Stück mit 2 Dips | Pommes | Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Sandwich mit Softgetränk">
        <meal>
          <name>Antipasti | Salami, Zucchini, Aubergine, Oliven | Käse</name>
          <note>Antioxidationsmittel</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Hafer</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Roggen</note>
          <note>Schwefeldioxid oder Sulfite</note>
          <note>Sesamsamen</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <note>geschwefelt</note>
          <note>geschwärzt</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Putenbraten in Currymarinade | Curry-Mango-Dip | Kartoffelbällchen</name>
          <note>Eier</note>
          <note>Milch</note>
          <note>Senf</note>
          <price role="other">6.00</price>
          <price role="student">4.50</price>
        </meal>
      </category>
      <category name="Hauptbeilagen">
        <meal>
          <name>Pommes Frites oder Penne Rigate</name>
          <note>Gluten</note>
          <note>Weizen</note>
        </meal>
      </category>
      <category name="Nebenbeilage">
        <meal>
          <name>Kaisergemüse oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-12-06">
      <category name="Tellergericht">
        <meal>
          <name>Bulgureintopf mit Kichererbsen und Gemüse | Fladenbrot</name>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">3.30</price>
          <price role="student">1.80</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Käsespätzle mit Haselnüssen | Käsesauce</name>
          <note>Dinkel</note>
          <note>Eier</note>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Haselnüsse</note>
          <note>Milch</note>
          <note>Schalenfrüchte</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="other">3.60</price>
          <price role="student">2.10</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Grillteller | Schwein, Putenbrust, Nürnberger Würstchen | Kräuterbutter | Grilltomate</name>
          <note>Antioxidationsmittel</note>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Phosphat</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <price role="other">5.40</price>
          <price role="student">3.90</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Hähnchenspieß | Erdnusssauce</name>
          <note>Erdnüsse</note>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
        <meal>
          <name>Hähnchenspieß | mediterrane Paprika-Zucchini-Sauce | Erdnusssauce</name>
          <note>Antioxidationsmittel</note>
          <note>Erdnüsse</note>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <note>geschwärzt</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Formaggio di Capra | Ziegenkäse, Honig</name>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Express">
        <meal>
          <name>Hähnchenspieß | mediterrane Paprika-Zucchini-Sauce | Erdnusssauce | Reis | Mischsalat</name>
          <note>Antioxidationsmittel</note>
          <note>Erdnüsse</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <note>geschwärzt</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Lasagne Bolognese | Béchamel</name>
          <note>Eier</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Vollkornspaghetti | Radicchio | Bärlauchpestosauce</name>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Tortiglioni Salmone | Lachs, Gemüse | Tomatenrahmsauce</name>
          <note>Antioxidationsmittel</note>
          <note>Fische</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Chinesische Wokpfanne | Garnelen, Gemüse | Basmatireis</name>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Krebstiere</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
        <meal>
          <name>Gemüse-Wok China-Art | Basmatireis</name>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
      </category>
      <category name="Burger Classics mit Pommes und Softgetränk">
        <meal>
          <name>Hamburger | Pommes | Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Cheeseburger | Pommes | Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Chicken Burger | Pommes | Getränk 0,25 L</name>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Veggieburger | Pommes | Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
      </category>
      <category name="Burger des Tages mit Pommes und Softgetränk">
        <meal>
          <name>Gorgonzola-Bacon-Burger | Laugenbrötchen, Preiselbeeren, Rucola</name>
          <note>Antioxidationsmittel</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">6.90</price>
          <price role="student">5.40</price>
        </meal>
      </category>
      <category name="Fingerfood mit Pommes und Softgetränk">
        <meal>
          <name>Chicken Wings 6 Stück mit einem Dip | Pommes | Getränk 0,25 L</name>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Hähnchennuggets 9 Stück mit 2 Dips | Pommes | Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Sandwich mit Softgetränk">
        <meal>
          <name>Caesar Style | Hähnchen, Oliven, Speck | Käse</name>
          <note>Antioxidationsmittel</note>
          <note>Eier</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Hafer</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Roggen</note>
          <note>Sesamsamen</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <note>geschwärzt</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Kasselerbraten | Bratensauce | Spätzle</name>
          <note>Antioxidationsmittel</note>
          <note>Eier</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Phosphat</note>
          <note>Weizen</note>
          <price role="other">6.00</price>
          <price role="student">4.50</price>
        </meal>
      </category>
      <category name="Hauptbeilagen">
        <meal>
          <name>Reis oder Spätzle</name>
          <note>Eier</note>
          <note>Gluten</note>
          <note>Weizen</note>
        </meal>
      </category>
      <category name="Nebenbeilage">
        <meal>
          <name>Prinzessbohnen oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-12-07">
      <category name="Tellergericht">
        <meal>
          <name>Maronen Suppe | Apfel-Nuss-Topping</name>
          <note>Schalenfrüchte</note>
          <note>Schwefeldioxid oder Sulfite</note>
          <note>Sojabohnen</note>
          <note>Walnüsse</note>
          <price role="other">3.30</price>
          <price role="student">1.80</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Blumenkohlnuggets | Joghurtdip</name>
          <note>Eier</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Weizen</note>
          <price role="other">3.60</price>
          <price role="student">2.10</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Rinderbraten mit Schmorgemüse</name>
          <note>Sellerie</note>
          <note>Senf</note>
          <price role="other">5.40</price>
          <price role="student">3.90</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Spaghetti Bolognese | ital. Hartkäse</name>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Pomodori fresco e Mozzarella | Tomaten, Mozzarella</name>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Express">
        <meal>
          <name>Spaghetti Bolognese | ital. Hartkäse | Mischsalat</name>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Nudelauflauf Siciliana | Hähnchen, Gemüse, Oliven | Tomatensauce</name>
          <note>Antioxidationsmittel</note>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Tortiglioni | Hirtenkäse, Rucola | Béchamel</name>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Spaghetti Lardo | Geflügel, Speck, Weißweinsauce | Tomatensauce</name>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Schwefeldioxid oder Sulfite</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Indonesische Nudeln mit Hähnchenstreifenstreifen</name>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
        <meal>
          <name>Mie Nudeln Indonesischer Art</name>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
      </category>
      <category name="Burger Classics mit Pommes und Softgetränk">
        <meal>
          <name>Hamburger | Pommes | Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Cheeseburger | Pommes | Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Chicken Burger | Pommes | Getränk 0,25 L</name>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Veggieburger | Pommes | Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
      </category>
      <category name="Burger des Tages mit Pommes und Softgetränk">
        <meal>
          <name>Gorgonzola-Bacon-Burger | Laugenbrötchen, Preiselbeeren, Rucola</name>
          <note>Antioxidationsmittel</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">6.90</price>
          <price role="student">5.40</price>
        </meal>
      </category>
      <category name="Fingerfood mit Pommes und Softgetränk">
        <meal>
          <name>Chicken Wings 6 Stück mit einem Dip | Pommes | Getränk 0,25 L</name>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Hähnchennuggets 9 Stück mit 2 Dips | Pommes | Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Sandwich mit Softgetränk">
        <meal>
          <name>Wiener Gaudi | Schnitzel, Krautsalat | Käse</name>
          <note>Eier</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Hafer</note>
          <note>Milch</note>
          <note>Roggen</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Zitronen-Knoblauch-Hähnchen | Aioli | Thymiankartoffeln</name>
          <note>Eier</note>
          <note>Milch</note>
          <note>Senf</note>
          <price role="other">6.00</price>
          <price role="student">4.50</price>
        </meal>
      </category>
      <category name="Hauptbeilagen">
        <meal>
          <name>Pariser Kartoffeln oder Spaghetti</name>
          <note>Gluten</note>
          <note>Weizen</note>
        </meal>
      </category>
      <category name="Nebenbeilage">
        <meal>
          <name>Buntes Gemüse oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-12-08">
      <category name="Vegetarisch">
        <meal>
          <name>Kürbis-Chia-Taler | Texicanasauce</name>
          <price role="other">3.60</price>
          <price role="student">2.10</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Chicken Tikka Massala Art | Paprikagemüse | Basmatireis</name>
          <note>Milch</note>
          <price role="other">5.40</price>
          <price role="student">3.90</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Schlemmerfilet Brokkoli | Weißweinsauce</name>
          <note>Fische</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Schwefeldioxid oder Sulfite</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Pancetta e funghi | Speck, Pilze | Sahnesauce</name>
          <note>Antioxidationsmittel</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Tellergericht">
        <meal>
          <name>Milchreis mit Beeren</name>
          <note>Milch</note>
          <price role="other">3.00</price>
          <price role="student">1.50</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Cannelloni | Rindfleisch | Tomatensauce</name>
          <note>Eier</note>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Gnocchi Genovese | Basilikum | Pfannengemüse | Pestorahmsauce</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Conchiglie Español | Chorizowurst, Paprika | Tomatensauce</name>
          <note>Antioxidationsmittel</note>
          <note>Eier</note>
          <note>Farbstoff</note>
          <note>Geschmacksverstärker</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Phosphat</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Gebratenes Rindfleisch mit Ananas | Curryreis</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
        <meal>
          <name>Gemüse-Ananas-Wok | Curryreis</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
      </category>
      <category name="Burger Classics mit Pommes und Softgetränk">
        <meal>
          <name>Hamburger | Pommes | Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Cheeseburger | Pommes | Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Chicken Burger | Pommes | Getränk 0,25 L</name>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
        <meal>
          <name>Veggieburger | Pommes | Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">5.80</price>
          <price role="student">4.30</price>
        </meal>
      </category>
      <category name="Burger des Tages mit Pommes und Softgetränk">
        <meal>
          <name>Gorgonzola-Bacon-Burger | Laugenbrötchen, Preiselbeeren, Rucola</name>
          <note>Antioxidationsmittel</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">6.90</price>
          <price role="student">5.40</price>
        </meal>
      </category>
      <category name="Fingerfood mit Pommes und Softgetränk">
        <meal>
          <name>Chicken Wings 6 Stück mit einem Dip | Pommes | Getränk 0,25 L</name>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
        <meal>
          <name>Hähnchennuggets 9 Stück mit 2 Dips | Pommes | Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <price role="other">5.00</price>
          <price role="student">3.50</price>
        </meal>
      </category>
      <category name="Sandwich mit Softgetränk">
        <meal>
          <name>Thunfisch | Salat, Paprika, Oliven | Käse</name>
          <note>Eier</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Hafer</note>
          <note>Milch</note>
          <note>Roggen</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <note>geschwärzt</note>
          <price role="other">4.70</price>
          <price role="student">3.20</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Putenbraten in Kräutermarinade | Kräuterschmand | Kartoffelwedges</name>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <price role="other">6.00</price>
          <price role="student">4.50</price>
        </meal>
      </category>
      <category name="Hauptbeilagen">
        <meal>
          <name>Kartoffelpüree oder Vollkornreis</name>
          <note>Milch</note>
        </meal>
      </category>
      <category name="Nebenbeilage">
        <meal>
          <name>Leipziger Allerlei oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-12-11">
      <category name="Tellergericht">
        <meal>
          <name>Nudelsuppe Persische Art | Fladenbrot</name>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="other">3.30</price>
          <price role="student">1.80</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Riesenrösti | Champignonrahmsauce</name>
          <note>Schwefeldioxid oder Sulfite</note>
          <note>Sojabohnen</note>
          <price role="other">3.60</price>
          <price role="student">2.10</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Schweinerückensteak | Sauce Robert</name>
          <note>Senf</note>
          <note>Süßungsmittel</note>
          <price role="other">5.40</price>
          <price role="student">3.90</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Hähnchennuggets | Curry-Mango-Dip</name>
          <note>6 Stk</note>
          <note>Eier</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Express">
        <meal>
          <name>Hähnchennuggets | Curry-Mango-Dip | Reis | Pariser Karotten</name>
          <note>6 Stk</note>
          <note>Eier</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Hauptbeilagen">
        <meal>
          <name>Schnittlauchkartoffeln oder Reis</name>
        </meal>
      </category>
      <category name="Nebenbeilage">
        <meal>
          <name>Pariser Karotten oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-12-12">
      <category name="Tellergericht">
        <meal>
          <name>Thaisuppe Tom Kha Gai | Kokosmilch, Hähnchen | Fladenbrot</name>
          <note>Gluten</note>
          <note>Sesamsamen</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">3.30</price>
          <price role="student">1.80</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Kichererbsen-Spinat-Curry | Süßkartoffelwürfel</name>
          <note>Antioxidationsmittel</note>
          <note>Konservierungsstoff</note>
          <price role="other">3.60</price>
          <price role="student">2.10</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Rindergeschnetzeltes | Waldpilzen | Rotweinsauce</name>
          <note>Schwefeldioxid oder Sulfite</note>
          <price role="other">5.40</price>
          <price role="student">3.90</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Schweineschnitzel | Pfeffersauce</name>
          <note>Eier</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Express">
        <meal>
          <name>Schweineschnitzel | Pfeffersauce | Pommes frites | Mais</name>
          <note>Eier</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Hauptbeilagen">
        <meal>
          <name>Pommes Frites oder Zartweizen</name>
          <note>Gluten</note>
          <note>Weizen</note>
        </meal>
      </category>
      <category name="Nebenbeilage">
        <meal>
          <name>Mais oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-12-13">
      <category name="Tellergericht">
        <meal>
          <name>Bohneneintopf | Paprika, Oliven | Weizenmischbrot</name>
          <note>Antioxidationsmittel</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Roggen</note>
          <note>Weizen</note>
          <note>geschwärzt</note>
          <price role="other">3.30</price>
          <price role="student">1.80</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Blumenkohlgratin | Gorgonzolasauce | Heidelbeerquark</name>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Weizen</note>
          <price role="other">3.60</price>
          <price role="student">2.10</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Schweinesteaks Saté | Asiatischen Gemüsenudeln | Erdnusssauce</name>
          <note>Erdnüsse</note>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">5.40</price>
          <price role="student">3.90</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Fleischbällchen | Orientalischer Tomatensauce</name>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Express">
        <meal>
          <name>Fleischbällchen | Orientalischer Tomatensauce | Vollkornreis | Mischsalat</name>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Hauptbeilagen">
        <meal>
          <name>Kartoffelpüree oder Vollkornreis</name>
          <note>Milch</note>
        </meal>
      </category>
      <category name="Nebenbeilage">
        <meal>
          <name>Fingermöhrchen oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-12-14">
      <category name="Tellergericht">
        <meal>
          <name>Currywurstsuppe | Paprika, Kartoffeln | Brötchen</name>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="other">3.30</price>
          <price role="student">1.80</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Scharfes Kürbisgemüse | Linsen, Rucola | Penne Rigate</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <price role="other">3.60</price>
          <price role="student">2.10</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Hähnchenbrust mit Zwiebel-Senf-Kruste | Bratensauce</name>
          <note>Gluten</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">5.40</price>
          <price role="student">3.90</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Frikadelle | Bratensauce</name>
          <note>Eier</note>
          <note>Gluten</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Express">
        <meal>
          <name>Frikadelle | Bratensauce | Pariser Kartoffeln | Buntes Bohnengemüse</name>
          <note>Eier</note>
          <note>Gluten</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Hauptbeilagen">
        <meal>
          <name>Pariser Kartoffeln oder Penne Rigate</name>
          <note>Gluten</note>
          <note>Weizen</note>
        </meal>
      </category>
      <category name="Nebenbeilage">
        <meal>
          <name>Buntes Bohnengemüse oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-12-15">
      <category name="Vegetarisch">
        <meal>
          <name>Vollkornreispfanne | Paprika | Sojagyros | Ayvar</name>
          <note>Sellerie</note>
          <note>Sojabohnen</note>
          <price role="other">3.60</price>
          <price role="student">2.10</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Mediterrane Hähnchenpfanne mit Mandel-Brokkoli und Kurkumareis</name>
          <note>Mandeln</note>
          <note>Milch</note>
          <note>Schalenfrüchte</note>
          <note>geschwärzt</note>
          <price role="other">5.40</price>
          <price role="student">3.90</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Backfisch | Kräutermayonnaise</name>
          <note>Eier</note>
          <note>Fische</note>
          <note>Gerste</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Tellergericht">
        <meal>
          <name>Germknödel | Vanillesauce</name>
          <note>Eier</note>
          <note>Farbstoff</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Weizen</note>
          <price role="other">3.00</price>
          <price role="student">1.50</price>
        </meal>
      </category>
      <category name="Express">
        <meal>
          <name>geschlossen</name>
          <price role="other">4.10</price>
          <price role="student">2.60</price>
        </meal>
      </category>
      <category name="Hauptbeilagen">
        <meal>
          <name>Pommes Frites oder Vollkornreis</name>
        </meal>
      </category>
      <category name="Nebenbeilage">
        <meal>
          <name>Mandel-Brokkoli oder Mischsalat</name>
          <note>Mandeln</note>
          <note>Schalenfrüchte</note>
        </meal>
      </category>
    </day>
  </canteen>
</openmensa>
"""
