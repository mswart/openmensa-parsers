from aachen import parse_url


def test_for_regression():
    assert parse_url(
        "https://web.archive.org/web/20170807225026/http://www.studierendenwerk-aachen.de/speiseplaene/academica-w.html",
        False) == """<?xml version="1.0" encoding="UTF-8"?>
<openmensa version="2.1" xmlns="http://openmensa.org/open-mensa-v2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd">
  <canteen>
    <day date="2017-08-07">
      <category name="Tellergericht">
        <meal>
          <name>Ostfrieseneintopf mit Rinderhack und Käse , Brötchen</name>
          <note>Farbstoff</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">1.80</price>
          <price role="other">3.30</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Hirtenkäse im Knuspermantel  mit Tomatensauce</name>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Weizen</note>
          <price role="student">2.10</price>
          <price role="other">3.60</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>*mensaVital* Feuriges Gemüse-Fischcurry  mit Ingwerreis</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Fische</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Weizen</note>
          <price role="student">3.90</price>
          <price role="other">5.40</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Hackbraten vom Schwein  mit Rahmsauce</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Eier</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Milch</note>
          <price role="student">2.60</price>
          <price role="other">4.10</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Rucola mit Tomaten, Parmesino und Knoblauch</name>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Kartoffel-Quark-Pierogi  mit Rote-Bete-Salat</name>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Süßungsmittel</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Pasta  Paprika mit Käse  und Paprikasauce</name>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Conchiglie  &quot;Prosciutto e Parmigiano&quot; mit Schinken, Käse , Parmesan  und Pestosauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Farbstoff</note>
          <note>Milch</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Thai-Curry mit Schweinefleisch, Paprika und Erdnusssauce , Korianderreis</name>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Erdnüsse</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Burger Classic">
        <meal>
          <name>Hamburger , Cheeseburger , Chicken Burger , Veggieburger  mit Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <price role="student">4.30</price>
          <price role="other">5.80</price>
        </meal>
      </category>
      <category name="Burger des Tages">
        <meal>
          <name>Pulled Pork-Burger mit Emmentaler im Laugen-Brötchen , Pommes und Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">5.40</price>
          <price role="other">6.90</price>
        </meal>
      </category>
      <category name="Fingerfood">
        <meal>
          <name>Frühlingsrollen  mit süß-sauer-Dip, Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Sandwich">
        <meal>
          <name>Club Style mit Hähnchen, Speck, frischem Salat, Oliven  und Käse</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>geschwärzt</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Roggen</note>
          <note>Gerste</note>
          <note>Hafer</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Mexikanisch gewürzter Schweinebraten  mit feuriger Sauce, Süßkartoffel Pommes frites</name>
          <note>Konservierungsstoff</note>
          <note>geschwefelt</note>
          <note>Senf</note>
          <note>Schwefeldioxid oder Sulfite</note>
          <price role="student">4.50</price>
          <price role="other">6.00</price>
        </meal>
      </category>
      <category name="Hauptbeilage">
        <meal>
          <name>Kartoffelpüree  oder Reis</name>
          <note>Milch</note>
        </meal>
      </category>
      <category name="Gemüse/Salat">
        <meal>
          <name>Mandel-Brokkoli  oder Mischsalat</name>
          <note>Schalenfrüchte</note>
          <note>Mandeln</note>
        </meal>
      </category>
    </day>
    <day date="2017-08-08">
      <category name="Tellergericht">
        <meal>
          <name>Bauerntopf mit Speck und Bohnen  mit Weizenmischbrot  mit Mettwurst</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Sellerie</note>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Roggen</note>
          <note>Gerste</note>
          <price role="student">1.80</price>
          <price role="other">3.30</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Falafel   mit Knoblauchdip</name>
          <note>vegan</note>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Senf</note>
          <price role="student">2.10</price>
          <price role="other">3.60</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Griechisches Hacksteak  mit Käsefüllung , scharfer Tomaten Sauce und Gurkensalat</name>
          <note>Rind und Schwein</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Milch</note>
          <note>Weizen</note>
          <price role="student">3.90</price>
          <price role="other">5.40</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Hähnchenschnitzel  mit Pusztasauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Antioxidationsmittel</note>
          <note>geschwefelt</note>
          <note>Süßungsmittel</note>
          <note>Schwefeldioxid oder Sulfite</note>
          <price role="student">2.60</price>
          <price role="other">4.10</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza BBQ Chicken mit Hähnchen, Paprikastreifen &amp; BBQ Sauce</name>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Geschmacksverstärker</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Farfalloni  &quot;Verdure&quot; mit Gemüse, Käse , Tomatensauce und Béchamel</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Sellerie</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Vollkornspaghetti  &quot;Carciofo&quot; mit Artischocken, Oliven  und Tomatenrahmsauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>geschwärzt</note>
          <note>Milch</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Bandnudeln  &quot;Salmone e Crema&quot; mit Lachs  und Béchamel</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Fische</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Hähnchenfleisch Kanton mit Paprika, Chinakohl, Sojasprossen mit Mienudeln , Mienudeln , auch vegetarisch erhältlich</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Burger Classic">
        <meal>
          <name>Hamburger , Cheeseburger , Chicken Burger , Veggieburger  mit Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <price role="student">4.30</price>
          <price role="other">5.80</price>
        </meal>
      </category>
      <category name="Burger des Tages">
        <meal>
          <name>Pulled Pork-Burger mit Emmentaler im Laugen-Brötchen , Pommes und Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">5.40</price>
          <price role="other">6.90</price>
        </meal>
      </category>
      <category name="Fingerfood">
        <meal>
          <name>Frühlingsrollen  mit süß-sauer-Dip, Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Sandwich">
        <meal>
          <name>Steakhouse Style mit Rindfleisch, Salat, Paprika, Oliven  und Käse</name>
          <note>geschwärzt</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Roggen</note>
          <note>Gerste</note>
          <note>Hafer</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Asiatisch marinierter Putenbraten mit Ingwer &amp; Honig, Korianderreis mit Erdnusssauce</name>
          <note>Farbstoff</note>
          <note>Erdnüsse</note>
          <price role="student">4.50</price>
          <price role="other">6.00</price>
        </meal>
      </category>
      <category name="Hauptbeilage">
        <meal>
          <name>Kräuter-Kartoffeln oder Penne Rigate</name>
          <note>Gluten</note>
          <note>Weizen</note>
        </meal>
      </category>
      <category name="Gemüse/Salat">
        <meal>
          <name>Leipziger Allerlei oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-08-09">
      <category name="Tellergericht">
        <meal>
          <name>Aramäische Rote Linsen Suppe  mit Reis, Fladenbrot</name>
          <note>vegan</note>
          <note>Gluten</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <price role="student">1.80</price>
          <price role="other">3.30</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Holländischer Stamppot  mit Gemüsefrikadellen</name>
          <note>Milch</note>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Weizen</note>
          <price role="student">2.10</price>
          <price role="other">3.60</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Schweinerückensteak mit Zwiebel-Senf-Kruste  und Balsamicojus</name>
          <note>Gluten</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>geschwefelt</note>
          <note>Schwefeldioxid oder Sulfite</note>
          <price role="student">3.90</price>
          <price role="other">5.40</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Currywurst   mit Röstzwiebeln</name>
          <note>Schwein</note>
          <note>Antioxidationsmittel</note>
          <note>Phosphat</note>
          <note>Gluten</note>
          <note>Weizen</note>
          <price role="student">2.60</price>
          <price role="other">4.10</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Rhodos mit Spinat, Hirtenkäse und Zwiebeln</name>
          <note>geschwärzt</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Maccheroni  &quot;Polpette&quot; mit Fleischbällchen , Gemüse  und Tomatensauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Rind</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Spaghetti  &quot;Gorgonzola e Pera&quot; mit Rucola, Birnen  und Gorgonzolasauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Farfalloni  &quot;Rosati&quot; mit Hähnchen, getrockneten Tomaten, Pesto  und Tomatensauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Rindfleisch mit Zwiebeln , Basmatireis, auch vegetarisch erhältlich</name>
          <note>Konservierungsstoff</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Burger Classic">
        <meal>
          <name>Hamburger , Cheeseburger , Chicken Burger , Veggieburger  mit Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <price role="student">4.30</price>
          <price role="other">5.80</price>
        </meal>
      </category>
      <category name="Burger des Tages">
        <meal>
          <name>Pulled Pork-Burger mit Emmentaler im Laugen-Brötchen , Pommes und Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">5.40</price>
          <price role="other">6.90</price>
        </meal>
      </category>
      <category name="Fingerfood">
        <meal>
          <name>Frühlingsrollen  mit süß-sauer-Dip, Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Sandwich">
        <meal>
          <name>Sweet Chili Chicken mit Hähnchenfleisch, Karotte  und Käse</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Roggen</note>
          <note>Gerste</note>
          <note>Hafer</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Schweinebraten &quot;mediterran&quot;  mit Knoblauchsauce  und Olivenöl-Kartoffeln</name>
          <note>Geschmacksverstärker</note>
          <note>Eier</note>
          <note>Senf</note>
          <note>geschwärzt</note>
          <price role="student">4.50</price>
          <price role="other">6.00</price>
        </meal>
      </category>
      <category name="Hauptbeilage">
        <meal>
          <name>Lyonerkartoffeln oder Vollkornreis</name>
        </meal>
      </category>
      <category name="Gemüse/Salat">
        <meal>
          <name>Buntes Möhrengemüse oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-08-10">
      <category name="Tellergericht">
        <meal>
          <name>*mensaVital* Couscous-Tomaten-Rucola-Salat mit Schweinefleisch</name>
          <note>Farbstoff</note>
          <note>geschwefelt</note>
          <note>Gluten</note>
          <note>Schwefeldioxid oder Sulfite</note>
          <note>Weizen</note>
          <price role="student">1.80</price>
          <price role="other">3.30</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Sojageschnetzeltes Stroganoff Art</name>
          <note>vegan</note>
          <note>Süßungsmittel</note>
          <note>Sojabohnen</note>
          <price role="student">2.10</price>
          <price role="other">3.60</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Lachsfilet  mit Zitronenhollandaise</name>
          <note>Gluten</note>
          <note>Fische</note>
          <note>Weizen</note>
          <note>Sellerie</note>
          <note>Eier</note>
          <note>Milch</note>
          <price role="student">3.90</price>
          <price role="other">5.40</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Rindergeschnetzeltes Jäger-Art mit Champignons</name>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="student">2.60</price>
          <price role="other">4.10</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Tonno mit Thunfisch, Zwiebeln, Knoblauch, Ital. Käse</name>
          <note>Gluten</note>
          <note>Fische</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Spaghetti  al Forno mit Tomaten, Pilzen, Speck  und Tomatensauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Milch</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Gnocchi  &quot;Siciliana&quot; mit Ratatouillegemüse, Oliven  und Tomatensauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>geschwärzt</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Penne  con Broccoli mit Hähnchen, Brokkoli  und Béchamel</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Grüner Thai Curry mit Garnelen  mit Basmatireis, auch vegetarisch erhältlich</name>
          <note>Gluten</note>
          <note>Krebstiere</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Burger Classic">
        <meal>
          <name>Hamburger , Cheeseburger , Chicken Burger , Veggieburger  mit Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <price role="student">4.30</price>
          <price role="other">5.80</price>
        </meal>
      </category>
      <category name="Burger des Tages">
        <meal>
          <name>Pulled Pork-Burger mit Emmentaler im Laugen-Brötchen , Pommes und Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">5.40</price>
          <price role="other">6.90</price>
        </meal>
      </category>
      <category name="Fingerfood">
        <meal>
          <name>Frühlingsrollen  mit süß-sauer-Dip, Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Sandwich">
        <meal>
          <name>Italian Style mit Salami, Rucola, Oliven und Grana Padano  und Käse</name>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>geschwefelt</note>
          <note>geschwärzt</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Sesamsamen</note>
          <note>Schwefeldioxid oder Sulfite</note>
          <note>Weizen</note>
          <note>Roggen</note>
          <note>Gerste</note>
          <note>Hafer</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Halbes Hähnchen &quot;St. Louis&quot; mit braunem Zucker, BBQ-Sauce  mit Curly Fries</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <price role="student">4.50</price>
          <price role="other">6.00</price>
        </meal>
      </category>
      <category name="Hauptbeilage">
        <meal>
          <name>Kartoffelpüree mit Röstzwiebeln Wellenbandnudeln</name>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Eier</note>
        </meal>
      </category>
      <category name="Gemüse/Salat">
        <meal>
          <name>Prinzessbohnen oder Krautsalat oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-08-11">
      <category name="Süßspeise">
        <meal>
          <name>Grießbrei mit Kirschen</name>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Weizen</note>
          <price role="student">1.50</price>
          <price role="other">3.00</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Überbackenes Riesenrösti  mit Kräuterrahmsauce</name>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Gerste</note>
          <price role="student">2.10</price>
          <price role="other">3.60</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>*mensaVital* Moussaka mit Rindfleisch  und Radieschen-Sprossensalat</name>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Sojabohnen</note>
          <note>Senf</note>
          <price role="student">3.90</price>
          <price role="other">5.40</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Backfisch  mit Kräutermayonnaise</name>
          <note>Gluten</note>
          <note>Fische</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Sellerie</note>
          <note>Eier</note>
          <note>Gerste</note>
          <price role="student">2.60</price>
          <price role="other">4.10</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Gorgonzola e Pera mit Gorgonzola und Birne</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Gnocchi  al forno mit Brokkoli, Kochschinken , Käse  und Béchamel</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Schwein</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Phosphat</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Maccheroni  &quot;Classica&quot; mit Blattspinat, ital. Hartkäse  und Béchamel</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Pasta  &quot;Amatriciana&quot; mit Speck, Oliven  und Tomatensauce</name>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Weizen</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>geschwärzt</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Hähnchenfleisch Kanpur mit gerösteten Erdnüssen und Gemüse , Ananas-Curry-Reis, auch vegetarisch erhältlich</name>
          <note>Gluten</note>
          <note>Erdnüsse</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Burger Classic">
        <meal>
          <name>Hamburger , Cheeseburger , Chicken Burger , Veggieburger  mit Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <price role="student">4.30</price>
          <price role="other">5.80</price>
        </meal>
      </category>
      <category name="Burger des Tages">
        <meal>
          <name>Pulled Pork-Burger mit Emmentaler im Laugen-Brötchen , Pommes und Getränk 0,25 L</name>
          <note>Farbstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">5.40</price>
          <price role="other">6.90</price>
        </meal>
      </category>
      <category name="Fingerfood">
        <meal>
          <name>Frühlingsrollen  mit süß-sauer-Dip, Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Sandwich">
        <meal>
          <name>Hähnchen Teriyaki mit frischem Salat, Teriyakisauce  und Käse</name>
          <note>geschwärzt</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Roggen</note>
          <note>Gerste</note>
          <note>Hafer</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Schweinekrustenbraten vom Grill mit Malzbiersauce , Bratkartoffeln mit Speck</name>
          <note>Gluten</note>
          <note>Senf</note>
          <note>Gerste</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <price role="student">4.50</price>
          <price role="other">6.00</price>
        </meal>
      </category>
      <category name="Hauptbeilage">
        <meal>
          <name>Pariser Kartoffeln oder Gemüsereis</name>
          <note>Sellerie</note>
        </meal>
      </category>
      <category name="Gemüse/Salat">
        <meal>
          <name>Blumenkohl oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-08-14">
      <category name="Tellergericht">
        <meal>
          <name>Linseneintopf mit Speck  mit Bockwurst  , Brötchen</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Sellerie</note>
          <note>Schwein</note>
          <note>Geschmacksverstärker</note>
          <note>Phosphat</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">1.80</price>
          <price role="other">3.30</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Gemüse-Köttbullar  mit orientalischer Tomatensauce</name>
          <note>Eier</note>
          <price role="student">2.10</price>
          <price role="other">3.60</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Lammcurry mit Joghurt  und Reis</name>
          <note>Milch</note>
          <price role="student">3.90</price>
          <price role="other">5.40</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Hähnchen Döner-Art  mit Joghurtdip</name>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <price role="student">2.60</price>
          <price role="other">4.10</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Gamberetti mit Shrimps, Spinat, Knoblauch und Oliven</name>
          <note>Farbstoff</note>
          <note>geschwärzt</note>
          <note>Gluten</note>
          <note>Krebstiere</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Conchiglie  al forno mit Gemüse , Rinderhack  und Béchamel</name>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Weizen</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Gnocchi  &quot;Mediterranea&quot; mit Champignons, Spinat  und Béchamel</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Tortiglioni  &quot;Poletto&quot; mit Geflügel, Paprikasauce und Rucola</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Schweinefleisch &quot;Woyishau&quot; mit Aprikosen &amp; Pflaumen , Basmatireis, auch vegetarisch erhältlich</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Burger Classic">
        <meal>
          <name>Hamburger , Cheeseburger , Chicken Burger , Veggieburger  mit Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <price role="student">4.30</price>
          <price role="other">5.80</price>
        </meal>
      </category>
      <category name="Burger des Tages">
        <meal>
          <name>Gorgonzola-Bacon-Burger mit Preiselbeeren und Rucola im Laugenbrötchen</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">5.40</price>
          <price role="other">6.90</price>
        </meal>
      </category>
      <category name="Fingerfood">
        <meal>
          <name>Chicken Wings 6 Stück mit einem Dip, Pommes und Getränk 0,25 L</name>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Sandwich">
        <meal>
          <name>Elsässer Art mit Zwiebeln, Crème Fraîche &amp; Speck  und Käse</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Roggen</note>
          <note>Gerste</note>
          <note>Hafer</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Spießbraten vom Schwein mit Schmorzwiebeln und Lyoner Kartoffeln</name>
          <price role="student">4.50</price>
          <price role="other">6.00</price>
        </meal>
      </category>
      <category name="Hauptbeilage">
        <meal>
          <name>Lyonerkartoffeln oder Vollkornreis</name>
        </meal>
      </category>
      <category name="Gemüse/Salat">
        <meal>
          <name>Prinzessbohnen oder Krautsalat oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-08-15">
      <category name="Tellergericht">
        <meal>
          <name>Italienischer Nudelsalat mit Putenschinken und Tomaten</name>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Phosphat</note>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Weizen</note>
          <price role="student">1.80</price>
          <price role="other">3.30</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>*mensaVital* Scharfes Kürbisgemüse mit Linsen und Rucola  auf Penne Rigate</name>
          <note>vegan</note>
          <note>Gluten</note>
          <note>Weizen</note>
          <price role="student">2.10</price>
          <price role="other">3.60</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Schweinesteaks Saté mit Erdnusssauce  und asiatischen Gemüsenudeln</name>
          <note>Farbstoff</note>
          <note>Erdnüsse</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.90</price>
          <price role="other">5.40</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Schweineschnitzel  mit Jalapenos-Käsesauce</name>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Milch</note>
          <price role="student">2.60</price>
          <price role="other">4.10</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Erbaccie mit Gorgonzola, Broccoli und Spinat</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Lachslasagne Rahmspinat  und Tomatensauce</name>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Fische</note>
          <note>Milch</note>
          <note>Weizen</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Spaghetti  &quot;al Arrabiata&quot;  mit Tomaten-Chili-Sauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Antioxidationsmittel</note>
          <note>geschwärzt</note>
          <note>Konservierungsstoff</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Conchiglie  &quot;Funghi e Carne&quot; mit Pilzen, Schweinefleisch  mit Bechamelsauce  und Bratensauce</name>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Weizen</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Thai Red Curry mit Gemüse und Putenstreifen , Korianderreis, auch vegetarisch erhältlich</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Burger Classic">
        <meal>
          <name>Hamburger , Cheeseburger , Chicken Burger , Veggieburger  mit Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <price role="student">4.30</price>
          <price role="other">5.80</price>
        </meal>
      </category>
      <category name="Burger des Tages">
        <meal>
          <name>Gorgonzola-Bacon-Burger mit Preiselbeeren und Rucola im Laugenbrötchen</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">5.40</price>
          <price role="other">6.90</price>
        </meal>
      </category>
      <category name="Fingerfood">
        <meal>
          <name>Chicken Wings 6 Stück mit einem Dip, Pommes und Getränk 0,25 L</name>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Sandwich">
        <meal>
          <name>Antipasti mit Salami, Zucchini, Aubergine und Oliven  und Käse</name>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>geschwefelt</note>
          <note>geschwärzt</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Sesamsamen</note>
          <note>Schwefeldioxid oder Sulfite</note>
          <note>Weizen</note>
          <note>Roggen</note>
          <note>Gerste</note>
          <note>Hafer</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Putenbraten in Currymarinade mit Curry-Mango-Dip  und Kartoffelbällchen</name>
          <note>Eier</note>
          <note>Milch</note>
          <note>Senf</note>
          <price role="student">4.50</price>
          <price role="other">6.00</price>
        </meal>
      </category>
      <category name="Hauptbeilage">
        <meal>
          <name>Kartoffelpüree  oder Penne Rigate</name>
          <note>Milch</note>
          <note>Gluten</note>
          <note>Weizen</note>
        </meal>
      </category>
      <category name="Gemüse/Salat">
        <meal>
          <name>Fingermöhrchen oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-08-16">
      <category name="Tellergericht">
        <meal>
          <name>Möhreneintopf mit Speck  und Frikadelle</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Milch</note>
          <note>Schwein</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Senf</note>
          <note>Weizen</note>
          <price role="student">1.80</price>
          <price role="other">3.30</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Vegetarische Frühlingsrolle  mit Süß-Saure-Sauce</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Eier</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Konservierungsstoff</note>
          <note>Weizen</note>
          <price role="student">2.10</price>
          <price role="other">3.60</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>*mensaVital* Chicken Tikka Massala mit Paprikagemüse  und Basmatireis</name>
          <note>Milch</note>
          <price role="student">3.90</price>
          <price role="other">5.40</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Hähnchenspieß  auf mediterraner Paprika-Zucchini-Sauce</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <note>Antioxidationsmittel</note>
          <note>geschwärzt</note>
          <price role="student">2.60</price>
          <price role="other">4.10</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Ziegenkäse mit Honig</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Lasagne  Bolognese mit Rinderhack  und Béchamel</name>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Sellerie</note>
          <note>Senf</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Vollkornspaghetti  mit Radicchio  und Bärlauchpestosauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Tortiglioni  &quot;Salmone&quot; mit Lachs, Gemüse  und Tomatenrahmsauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Sellerie</note>
          <note>Fische</note>
          <note>Milch</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Chinesische Wokpfanne mit Garnelen und Gemüse , Basmatireis, auch vegetarisch erhältlich</name>
          <note>Gluten</note>
          <note>Krebstiere</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Burger Classic">
        <meal>
          <name>Hamburger , Cheeseburger , Chicken Burger , Veggieburger  mit Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Gerste</note>
          <price role="student">4.30</price>
          <price role="other">5.80</price>
        </meal>
      </category>
      <category name="Burger des Tages">
        <meal>
          <name>Gorgonzola-Bacon-Burger mit Preiselbeeren und Rucola im Laugenbrötchen</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">5.40</price>
          <price role="other">6.90</price>
        </meal>
      </category>
      <category name="Fingerfood">
        <meal>
          <name>Chicken Wings 6 Stück mit einem Dip, Pommes und Getränk 0,25 L</name>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Sandwich">
        <meal>
          <name>Caesar Style mit Hähnchen, Oliven, Speck  und Käse</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>geschwärzt</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Roggen</note>
          <note>Gerste</note>
          <note>Hafer</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Kasselerbraten  mit Bratensauce und Spätzle</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Phosphat</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Weizen</note>
          <price role="student">4.50</price>
          <price role="other">6.00</price>
        </meal>
      </category>
      <category name="Hauptbeilage">
        <meal>
          <name>Reis oder Bandnudeln</name>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Weizen</note>
        </meal>
      </category>
      <category name="Gemüse/Salat">
        <meal>
          <name>Kaisergemüse oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-08-17">
      <category name="Tellergericht">
        <meal>
          <name>*mensaVital* Kartoffel-Gemüse-Pfanne mit Putenbruststreifen und Curry-Frischkäse-Soße</name>
          <note>Milch</note>
          <price role="student">1.80</price>
          <price role="other">3.30</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Kichererbsen-Spinat-Curry mit Süßkartoffelwürfel</name>
          <note>vegan</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <price role="student">2.10</price>
          <price role="other">3.60</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Rinderbraten mit Schmorgemüse</name>
          <note>Sellerie</note>
          <note>Senf</note>
          <price role="student">3.90</price>
          <price role="other">5.40</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Spaghetti  Carbonara mit Putenschinken</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Phosphat</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <price role="student">2.60</price>
          <price role="other">4.10</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Pomodori fresco e Mozzarella mit Tomaten und Mozzarella</name>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Nudelauflauf  &quot;Siciliana&quot; mit Hähnchen, Gemüse, Oliven  und Tomatensauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Antioxidationsmittel</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Tortiglioni  Rucola mit Hirtenkäse  und Béchamel</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Milch</note>
          <note>Sellerie</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Spaghetti  &quot;Lardo&quot; mit Geflügel, Speck, Weißwein-  und Tomatensauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Milch</note>
          <note>Schwefeldioxid oder Sulfite</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Indonesische Nudeln mit Putenstreifen , auch vegetarisch erhältlich</name>
          <note>Konservierungsstoff</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Burger Classic">
        <meal>
          <name>Hamburger , Chicken Burger , Cheeseburger , Veggieburger  mit Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <note>Farbstoff</note>
          <price role="student">4.30</price>
          <price role="other">5.80</price>
        </meal>
      </category>
      <category name="Burger des Tages">
        <meal>
          <name>Gorgonzola-Bacon-Burger mit Preiselbeeren und Rucola im Laugenbrötchen</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">5.40</price>
          <price role="other">6.90</price>
        </meal>
      </category>
      <category name="Fingerfood">
        <meal>
          <name>Chicken Wings 6 Stück mit einem Dip, Pommes und Getränk 0,25 L</name>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Sandwich">
        <meal>
          <name>Wiener Gaudi mit Schweineschnitzel, Krautsalat  und Käse</name>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Roggen</note>
          <note>Gerste</note>
          <note>Hafer</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Zitronen-Knoblauch-Hähnchen mit Aioli  und Thymiankartoffeln</name>
          <note>Eier</note>
          <note>Milch</note>
          <note>Senf</note>
          <price role="student">4.50</price>
          <price role="other">6.00</price>
        </meal>
      </category>
      <category name="Hauptbeilage">
        <meal>
          <name>Pariser Kartoffeln oder Spaghetti</name>
          <note>Gluten</note>
          <note>Weizen</note>
        </meal>
      </category>
      <category name="Gemüse/Salat">
        <meal>
          <name>Balkangemüse oder Mischsalat</name>
        </meal>
      </category>
    </day>
    <day date="2017-08-18">
      <category name="Süßspeise">
        <meal>
          <name>Milchreis mit Aprikosen</name>
          <note>Antioxidationsmittel</note>
          <note>Milch</note>
          <price role="student">1.50</price>
          <price role="other">3.00</price>
        </meal>
      </category>
      <category name="Vegetarisch">
        <meal>
          <name>Blumenkohlnuggets  mit Joghurtdip</name>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Weizen</note>
          <note>Milch</note>
          <price role="student">2.10</price>
          <price role="other">3.60</price>
        </meal>
      </category>
      <category name="Empfehlung des Tages">
        <meal>
          <name>Putenscaloppine mit Zitronensauce</name>
          <note>Milch</note>
          <price role="student">3.90</price>
          <price role="other">5.40</price>
        </meal>
      </category>
      <category name="Klassiker">
        <meal>
          <name>Schlemmerfilet Brokkoli  mit Weißweinsauce</name>
          <note>Gluten</note>
          <note>Fische</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Schwefeldioxid oder Sulfite</note>
          <price role="student">2.60</price>
          <price role="other">4.10</price>
        </meal>
      </category>
      <category name="Pizza des Tages">
        <meal>
          <name>Pizza Pancetta e funghi mit Speck &amp; Pilzen in Sahnesauce</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Pasta">
        <meal>
          <name>Cannelloni  mit Rindfleisch  und Tomatensauce</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Eier</note>
          <note>Milch</note>
          <note>Weizen</note>
          <note>Sojabohnen</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Gnocchi  &quot;Genovese&quot; mit Basilikum, Pfannengemüse  und Pestorahmsauce</name>
          <note>Gluten</note>
          <note>Weizen</note>
          <note>Sellerie</note>
          <note>Sojabohnen</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
        <meal>
          <name>Conchiglie  &quot;Español&quot; mit Chorizowurst vom Schwein, Paprika  und Tomatensauce</name>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Weizen</note>
          <note>Farbstoff</note>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Geschmacksverstärker</note>
          <note>Phosphat</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Wok">
        <meal>
          <name>Gebratenes Rindfleisch mit Ananas  mit Curryreis, auch vegetarisch erhältlich</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Sojabohnen</note>
          <note>Weizen</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Burger Classic">
        <meal>
          <name>Hamburger , Chicken Burger , Cheeseburger , Veggieburger  mit Pommes und Getränk 0,25 L</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <note>Farbstoff</note>
          <price role="student">4.30</price>
          <price role="other">5.80</price>
        </meal>
      </category>
      <category name="Burger des Tages">
        <meal>
          <name>Gorgonzola-Bacon-Burger mit Preiselbeeren und Rucola im Laugenbrötchen</name>
          <note>Konservierungsstoff</note>
          <note>Antioxidationsmittel</note>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Weizen</note>
          <note>Gerste</note>
          <price role="student">5.40</price>
          <price role="other">6.90</price>
        </meal>
      </category>
      <category name="Fingerfood">
        <meal>
          <name>Chicken Wings 6 Stück mit einem Dip, Pommes und Getränk 0,25 L</name>
          <price role="student">3.50</price>
          <price role="other">5.00</price>
        </meal>
      </category>
      <category name="Sandwich">
        <meal>
          <name>Thunfisch mit frischem Salat, Paprika, Oliven  und Käse</name>
          <note>geschwärzt</note>
          <note>Gluten</note>
          <note>Eier</note>
          <note>Fische</note>
          <note>Sojabohnen</note>
          <note>Milch</note>
          <note>Senf</note>
          <note>Sesamsamen</note>
          <note>Weizen</note>
          <note>Roggen</note>
          <note>Gerste</note>
          <note>Hafer</note>
          <price role="student">3.20</price>
          <price role="other">4.70</price>
        </meal>
      </category>
      <category name="Flammengrill">
        <meal>
          <name>Putenbraten in Kräutermarinade mit Kartoffelwedges und Kräuterschmand</name>
          <note>Gluten</note>
          <note>Sellerie</note>
          <note>Milch</note>
          <note>Gerste</note>
          <price role="student">4.50</price>
          <price role="other">6.00</price>
        </meal>
      </category>
      <category name="Hauptbeilage">
        <meal>
          <name>Pariser Kartoffeln oder Zartweizen</name>
          <note>Gluten</note>
          <note>Weizen</note>
        </meal>
      </category>
      <category name="Gemüse/Salat">
        <meal>
          <name>Blattspinat  oder Mischsalat</name>
          <note>Gluten</note>
          <note>Milch</note>
          <note>Weizen</note>
        </meal>
      </category>
    </day>
  </canteen>
</openmensa>
"""
