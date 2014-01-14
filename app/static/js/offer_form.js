(function(){

    var OfferView = window.ahr.item_form_base.extend({
        item:'',
        init:function(){
            this.url = window.ahr.app_urls.addmarketitem+'offer';
        },
        getFormData: function(){
            var that = this;
            var retdict={};
            retdict['skills'] = this.skills_widget.getTagIds();
            retdict['countries'] = this.countries_widget.getTagIds();
            retdict['issues'] = this.issues_widget.getTagIds();
            retdict['exp_date'] = this.expdate_widget.getExpDate();
            retdict['title'] = this.title_widget.getval();
            retdict['details'] = this.details_widget.getval();
            retdict.csrfmiddlewaretoken=$('input[name="csrfmiddlewaretoken"]').val();
            return retdict;
        },

        aftersubmit:function(){
            window.location = '/market';
        },

        makeWidget: function(){
            var that = this;
            this.issues_widget = window.ahr.typeahead_widget.initWidget(
                        '#issues_place',
                        {title:'I can help to advance freedom of:', jsonfield:'issues'},
                        this.item_obj);

            this.countries_widget = window.ahr.typeahead_widget.initWidget(
                        '#countries_place',
                        {title:'Please select the countries where you can help',  jsonfield:'countries'},
                        this.item_obj);

            this.skills_widget = window.ahr.typeahead_widget.initWidget(
                        '#skills_place',
                        {title:'Skills',  jsonfield:'skills'},
                        this.item_obj);

            this.expdate_widget = window.ahr.expdate_widget.initWidget(
                        '#exp_date_place',
                        {title:'Expires in days', jsonfield:'exp_date'},
                        this.item_obj);

            this.title_widget = window.ahr.input_widget.initWidget(
                        '#title_place',
                        {title:'Title of post', jsonfield:'title', placeholder:''},
                        this.item_obj? this.item_obj.title : null);

            this.details_widget = window.ahr.textarea_widget.initWidget(
                        '#details_place',
                        {title:'', jsonfield:'details', placeholder:'Please give details of what you can help with?'},
                        this.item_obj? this.item_obj.details : null);
        }
    });

    window.ahr.offer_form = window.ahr.offer_form|| {};
    window.ahr.offer_form.initItem= function(item){
        var offer_form = new OfferView(item);
    };
})();


