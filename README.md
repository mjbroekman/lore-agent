# lore-agent
A local agent for helping keep track of lore consistency in my writing and planning

# File Formats
Use markdown for the files that the agent will read in. Here's an example:

```
---
category: NPC
location: Ironforge Docks
status: Alive
faction: Silver Guild
---
# Hognar the Bold
Hognar is a retired mercenary...

## Relationships
* **Ally:** Elara the Swift
* **Enemy:** The Rat-King
```

Make sure each file corresponds to a single person, location, event, etc

# Tips for ensuring consistency

## Links between documents
If a character is mentioned in a location file, use the character's full unique name.

Bad: "The king lives here." (Which king?)
Good: "King Alaric III lives in the High Spire of Oakhaven."

## Format of files
Pick a template for your files and stick to it religiously. You can use different templates for each _type_ of data, but be sure to use the same template **within** a given type.

If you use Name: [Name] in one NPC file and Title: [Name] in another, the agent will struggle to recognize them as the same attribute.

## Global Summary
Create a _Global_Summary.md file with a 1-page overview of the entire world. This will be read first so it has the "big picture" before diving into specific chunks.

