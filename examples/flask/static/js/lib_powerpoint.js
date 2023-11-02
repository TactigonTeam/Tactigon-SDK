const blocks = [
  {
    "type": "powerpoint_gesture",
    "message0": "combo gesture %1 routine %2",
    "args0": [
      {
        "type": "input_value",
        "name": "gesture"
      },
      {
        "type": "input_value",
        "name": "routine",
        "check": "String"
      }
    ],
    "colour": 230,
    "tooltip": "",
    "helpUrl": ""
  },
  {
    "type": "powerpoint_tskin",
    "message0": "TSkin %1 %2 btn 1 %3 btn 2 %4 btn 3 %5",
    "args0": [
      {
        "type": "field_dropdown",
        "name": "hand",
        "options": [
          [
            "LEFT",
            "left"
          ],
          [
            "RIGHT",
            "right"
          ]
        ]
      },
      {
        "type": "input_dummy"
      },
      {
        "type": "input_value",
        "name": "button_1",
        "check": "powerpoint_button"
      },
      {
        "type": "input_value",
        "name": "button_2",
        "check": "powerpoint_button"
      },
      {
        "type": "input_value",
        "name": "button_3",
        "check": "powerpoint_button"
      }
    ],
    "colour": 230,
    "tooltip": "",
    "helpUrl": ""
  },
  {
    "type": "powerpoint_button",
    "message0": "Mode %1 %2 routine %3",
    "args0": [
      {
        "type": "field_dropdown",
        "name": "mode",
        "options": [
          [
            "sticky",
            "sticky"
          ],
          [
            "not sticky",
            "not-sticky"
          ]
        ]
      },
      {
        "type": "input_dummy"
      },
      {
        "type": "input_value",
        "name": "routine",
        "check": "String"
      }
    ],
    "output": null,
    "colour": 230,
    "tooltip": "",
    "helpUrl": ""
  } 
]

const tooblox =  {
  kind: "categoryToolbox",
  contents: [
    {
      kind: "category",
      name: "Base",
      categorystyle: "logic_category",
      contents: [
        {kind: "block", type: "text"},
        {kind: "block", type: "lists_create_with"},
      ]
    },
    {
      kind: "category",
      name: "Powerpoint",
      categorystyle: "math_category",
      contents: [
        {kind: "block", type: "powerpoint_gesture"},
        {kind: "block", type: "powerpoint_tskin"},
        {kind: "block", type: "powerpoint_button"},
      ]
    },
  ]
}


export {blocks, tooblox}