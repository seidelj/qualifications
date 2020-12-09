var cwas = new Vue({
    el: '#cont1',
    data: {
        active: errorExists ? 7 : 0
    },
    methods: {
        next: function() {
            this.active+=1
            document.body.scrollTop = 0; // For Safari
            document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
        },
        back: function() {
            this.active-=1
            document.body.scrollTop = 0; // For Safari
            document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
        },
        quiz: function() {
            this.active = 5
            document.body.scrollTop = 0;
            document.documentElement.scrollTop =0;
        },
        page: function(p) {
            this.active = p
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        },
    }
})
