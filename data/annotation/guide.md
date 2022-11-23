# Annotation Guideline

1. [How to create annotation and getting started](##-Guide)
2. [The description of each emotion](##-Emotion)
3. [How to download annotations and upload](##-When-you're-ready-to-upload-your-annotation)

## Guide to setup
- Launch label studio from the terminal:
  ```bash
  label-studio
  ```
- Create new project
- Under `Data Import` import `data/annotation/data.csv`. and pick "`List of Tasks`".
- Then pick the setup: Go to "Natural Language Processing" and choose "Text Classification". It will open an interface where you should go to `code` and replace the existing code with this [HTML CODE](##-HTML-CODE).
- Press `save`. 
- Start annotating!

## When you're done annotating
- Go to `Export` and export the annotations as `CSV` file.
- Rename the file to `yourname.csv` and upload to `data/annotation/annotated/yourname.csv` like this: `viktor.csv`
- For those needing git help:
  ```bash
  git add data/annotation/annotated/git commit -m "Added annotations"
  git push
  ```

## HTML CODE
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
</View>
```

## Emotions:
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