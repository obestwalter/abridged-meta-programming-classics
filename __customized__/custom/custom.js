// If you are not sure that this is loaded at all ...
// alert("hello world from custom.js");

define([
    'base/js/namespace',
    'base/js/events'
    ],
    function(IPython, events) {
        events.on("notebook_loaded.Notebook",
            function () {
                  IPython.notebook.set_autosave_interval(23000); //in milliseconds
            }
          );
        //may include additional events.on() statements
    }
);
