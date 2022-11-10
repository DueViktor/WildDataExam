# Annotation Guideline

**Emotions**:
- Knowledge: Exchange of ideas or information
- Power: Having power over the behavior and outcomes of another
- Status: Conferring status, appreciation, gratitude, or admiration upon another
- Trust: Will of relying on the actions or judgments of another
- Support: Giving emotional or practical aid and companionship
- Romance: Intimacy among people with a sentimental or sexual relationship
- Similarity: Shared interests, motivations or outlooks
- Identity: Shared sense of belonging to the same community or group community
- Fun: Experiencing leisure, laughter, and joy
- Conflict: Contrast or diverging views

## How to use Label studio
- Launch label studio
- Create new project
- Import "ready-to-annotate.csv" file from the "Label_studio" folder
- Use it as a "List of Tasks"
- To choose a setup: Go to "NLP" and choose "Text Classification" 
- Go to the "code" section and replace the existing code with the code html below:

### CODE TO USE IN LABEL STUDIO
``` html
<View>
  <Text name="text" value="$text"/>
  <View style="box-shadow: 2px 2px 5px #999;                padding: 20px; margin-top: 2em;                border-radius: 5px;">
    <Header value="Choose text sentiment"/>
    <Choices name="sentiment" toName="text" choice="multiple" showInLine="true">
      <Choice value="Knowledge" hint="hhhdede"/> 
      <Choice value="Support"/>
      <Choice value="Romance"/>
      <Choice value="Power"/>
      <Choice value="Status"/>
      <Choice value="Trust"/>
      <Choice value="Similarity"/>
      <Choice value="Identity"/>
      <Choice value="Fun"/>
      <Choice value="Conflict"/>
    </Choices>
  </View>
</View><!-- {
  "data": {"text": "This is a great 3D movie that delivers everything almost right in your face."}
} -->
```
