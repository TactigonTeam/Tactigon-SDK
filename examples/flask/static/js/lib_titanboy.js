const blocks = [
  {
    "type": "titanboy_phrase",
    "message0": "phrase %1 hotwords %2 audio feedback %3 error feedback %4 command %5",
    "args0": [
      {
        "type": "input_value",
        "name": "phrase",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "hotwords",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "audio_feedback",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "error_feedback",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "command",
        "align": "RIGHT",
        "check": "String"
      }
    ],
    "colour": 230,
    "tooltip": "",
    "helpUrl": ""
  },
  {
    "type": "titanboy_phrase_gesture",
    "message0": "phrase %1 gesture %2 hotwords %3 audio feedback %4 error feedback %5 command %6",
    "args0": [
      {
        "type": "input_value",
        "name": "phrase",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "gesture",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "hotwords",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "audio_feedback",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "error_feedback",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "command",
        "align": "RIGHT",
        "check": "String"
      }
    ],
    "colour": 230,
    "tooltip": "",
    "helpUrl": ""
  },
  {
    "type": "titanboy_phrase_combo_gesture",
    "message0": "phrase %1 left gesture %2 right gesture %3 hotwords %4 audio feedback %5 error feedback %6 command %7",
    "args0": [
      {
        "type": "input_value",
        "name": "phrase",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "gesture_l",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "gesture_r",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "hotwords",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "audio_feedback",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "error_feedback",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "command",
        "align": "RIGHT",
        "check": "String"
      }
    ],
    "colour": 230,
    "tooltip": "",
    "helpUrl": ""
  },
  {
    "type": "titanboy_ib_command",
    "message0": "left gesture %1 right gesture %2 command %3 voice %4",
    "args0": [
      {
        "type": "input_value",
        "name": "gesture_l",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "gesture_r",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "command",
        "check": "String",
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "voice",
        "align": "RIGHT",
        "check": "Boolean"
      }
    ],
    "colour": 230,
    "tooltip": "",
    "helpUrl": ""
  },
  
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
        {kind: "block", type: "math_number"},
        {kind: "block", type: "logic_boolean"},
        {kind: "block", type: "lists_create_with"},
      ]
    },
    {
      kind: "category",
      name: "Voice",
      categorystyle: "math_category",
      contents: [
        {kind: "block", type: "titanboy_phrase"},
        {kind: "block", type: "titanboy_phrase_gesture"},
        {kind: "block", type: "titanboy_phrase_combo_gesture"},
      ]
    },
    {
      kind: "category",
      name: "TitanBoy",
      categorystyle: "math_category",
      contents: [
        {kind: "block", type: "titanboy_ib_command"},
      ]
    },
  ]
}


export {blocks, tooblox}