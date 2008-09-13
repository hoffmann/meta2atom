=============================
meta2atom atom feed generator
=============================

meta2atom is a python script to generate atom feeds based ont the meta tags
in html documents.


HTML Meta Tags
--------------
::

    <title>document tiltel</title>
    <meta name="author" content="name"
    <meta name="description" content="content description">
    <meta name="keywords" content="comma, sep, keywords">
    <meta name="date" content="datetime">

    <meta http-equiv="content-language" content="de">

Dublin Core Meta Information
    ----------------------------t
::

    <meta name="DC.title" content="SELFHTML: Meta-Angaben">
    <meta name="DC.creator" content="Stefan M&uuml;nz">
    <meta name="DC.description" content="Heute bekannte Meta-Angaben in HTML">
    <meta name="DC.subject" content="Meta-Angaben">
    <meta name="DC.date" content="2001-12-15T08:49:37+02:00" scheme="DCTERMS.W3CDTF">
    
    <meta name="DC.language"    content="de">




Atom Feed
---------

* http://tools.ietf.org/html/rfc4287


::

    <entry>
    <author>
        <name> </name>
        <uri>  </uri>
        <email> </email>
    </author>
    <title> </title>
    <link rel="alternate" type="text/html" href="" />
    <id> </id>
    <updated> </updated>
    <published> </published>
    <category scheme="" term="" /><categorey scheme="" term="" />
    <summary> </summary>
    <content> </content>
    </entry>

