
function initializeBlockly(blocks, toolbox, save_state_endpoint, load_state_endpoint){
    Blockly.defineBlocksWithJsonArray(blocks)

    const options = {
        toolbox: toolbox,
        grid: {
            spacing: 20,
            length: 3,
            colour: '#e6e6e6',
        },
        zoom: {
            controls: true,
            wheel: true,
            startScale: 1.0,
            maxScale: 3,
            minScale: 0.3,
            scaleSpeed: 1.2,
            pinch: true
        },
        trashcan: true
    }
    
    const workspace = Blockly.inject('blocklyDiv', options);
    load_state(load_state_endpoint, workspace)

    // $("#load_workspace").click(function(e){
    //     load_state(workspace)
    // });
    
    $("#save_workspace").click(function(e){
        const serializer = new Blockly.serialization.blocks.BlockSerializer();
        const state = serializer.save(workspace);
        const state_string = JSON.stringify(state);
    
        $.ajax(save_state_endpoint, {
                method: "POST",
                contentType: "application/json; charset=utf-8",
                data: state_string,
                dataType: "json"
            }).done(function(res){
                console.log(res)
                console.log("salvato")
                window.location.reload()
            });

    });

}

function load_state(load_state_endpoint, workspace) {
    $.get(load_state_endpoint).done(function(res){
        const serializer = new Blockly.serialization.blocks.BlockSerializer();
        serializer.load(res, workspace)
    });
}

export { initializeBlockly };
