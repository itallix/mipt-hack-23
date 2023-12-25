Feature: Vision Pro can detect artwork
A model can correctly identify the artwork on the image

    @paintings
    Scenario Outline: Can detect paintings
      Given The painting "<filename>"
      When Gemini Pro Vision triggered
      Then The model response should match "<author> - <title>"

      Examples:
        | filename       | author           | title                     |
        | aivazovsky.jpg | Ivan Aivazovsky  | The Ninth Wave            |
        | dali.jpg       | Salvador Dali    | The Persistence of Memory |
        | monet1.jpg     | Claude Monet     | The Japanese Footbridge   |
        | monet2.jpg     | Claude Monet     | The Stroll at Giverny     |
        | picasso.jpg    | Pablo Picasso    | Women of Algiers          |
        | van_gogh1.jpg  | Vincent van Gogh | Noon Rest from Work       |
        | van_gogh2.jpg  | Vincent van Gogh | The Starry Night          |


    @landmarks
    Scenario Outline: Can detect landmarks
      Given The landmark "<filename>"
      When Gemini Pro Vision triggered
      Then The model response should match "<city> - <landmark>"

      Examples:
        | filename         | city             | landmark                |
        | colosseum.jpg    | Rome             | Colosseum               |
        | isaacs.jpg       | Saint Petersburg | Saint Isaac's Cathedral |
        | rushmore.jpg     | Keystone         | Mount Rushmore          |
        | taj_mahal.jpg    | Agra             | Taj Mahal               |
        | the_gate.jpg     | Berlin           | Brandenburg Gate        |
        | tower_bridge.jpg | London           | Tower Bridge            |
