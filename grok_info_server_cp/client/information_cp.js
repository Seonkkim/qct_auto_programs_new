function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++){
            var cookie = jQuery.trim(cookies[i]);
            if(cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)&/.test(method));
}
/*
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
*/
var result_sp, result_build;
var request;

var xhr = new XMLHttpRequest();

request = $.ajax({
    url: "https://automotive-linux:9999/db/sp/?category__in=LV,QX,HQX,LV_LE",
    type: "GET",
    cache: false,
    crossDomain: true,
    datatype: "json",
    async: false,
    xhrFields: {
      withCredentials: true
    },
    success: reqGetResponseSP,
    error: function(error) {
	console.log('error occured');
	console.log(error);
    }
});
request = $.ajax({
    url: "https://automotive-linux:9999/db/build/",
    type: "GET",
    cache: false,
    crossDomain: true,
    datatype: "json",
    async: false,
    xhrFields: {
      withCredentials: true
    },
    success: reqGetResponseBuild,
    error: function(error) {
	console.log('error occured');
	console.log(error);
    }
});
function reqGetResponseSP(data) {
    var result_sp_json = JSON.parse(JSON.stringify(data));
    result_sp = [];
    for(var x in result_sp_json) {
	result_sp.push(result_sp_json[x]);	
    }
}
function reqGetResponseBuild(data) {
    var result_build_json = JSON.parse(JSON.stringify(data));
    result_build = [];
    for(var x in result_build_json) {
	result_build.push(result_build_json[x]);
    }
    draw();
}
function open_releasenote(name, rno) {
    window.open('META_BUILD/'+ name + '/' + rno + '.pdf', '_blank', 'fullscreen=yes');
}
function draw() {
        var len_sp = result_sp.length;
        result_sp.sort(function(a, b) {
            var first = a['category'].localeCompare(b['category']);
	    var second = a['version'].localeCompare(b['version']);
	    if (first != 0) return first;
	    if (second != 0) return second;
 	    return 0;
        });
        result_build.sort(function(a, b) {
            return b['name'].localeCompare(a['name']);
        });
        //var menu = document.getElementsByClassName('menu')[0];
        var menu = document.getElementById("SP");
        //var len = data_sp.values.length;
        for(i = 0; i < len_sp; i++) {
            //var row = my_tbody.insertRow(my_tibody.rows.length);
            var entry = document.createElement('li');
            entry.setAttribute('class', 'menu');
            var pointer = document.createElement('span');
            pointer.setAttribute('class', 'pointer');
            pointer.innerHTML = "&#9656";
            entry.appendChild(pointer);
            var aTag = document.createElement('a');
            aTag.innerHTML = result_sp[i]['name'];
            aTag.setAttribute('style', 'font-weight:bold');
            entry.appendChild(aTag);
            //entry.createTextNode(result_sp[i][1]);
            menu.appendChild(entry);

            var wiki = result_sp[i]['wiki'];
            var wlink = document.createElement('a');
            var w_edit = document.createElement('a');
            var w_save = document.createElement('a');
            var w_cancel = document.createElement('a');
            var toptext = document.createElement('ol');
            toptext.setAttribute('class', 'hide');
            w_edit.setAttribute('class', 'edit');
            w_save.setAttribute('class', 'save');
            w_cancel.setAttribute('class', 'cancel');

            w_edit.setAttribute('style', 'color:gray; margin:3px');
            w_save.setAttribute('style', 'color:gray; margin:3px');
            w_cancel.setAttribute('style', 'color:gray; margin:3px');
            w_edit.innerHTML = "edit";
            w_save.innerHTML = "save";
            w_cancel.innerHTML = "cancel";

            wlink.setAttribute('href', wiki);
            wlink.setAttribute('style', 'color:blue; font-weight:bold');
            wlink.innerHTML = wiki;
            var wikitext = document.createElement('b');
            wikitext.setAttribute('style', 'color:black; font-weight:bold');
            wikitext.innerHTML = "Wiki: ";
            toptext.appendChild(wikitext);
            toptext.appendChild(wlink);
            toptext.appendChild(w_edit);
            toptext.appendChild(w_save);
            toptext.appendChild(w_cancel);
            var secondtext = document.createElement('ol');
            var b_project = document.createElement('b');
            var p_edit = document.createElement('a');
            var p_save = document.createElement('a');
            var p_cancel = document.createElement('a');
            p_edit.setAttribute('class', 'edit');
            p_save.setAttribute('class', 'save');
            p_cancel.setAttribute('class', 'cancel');

            p_edit.setAttribute('style', 'color:gray; margin:3px');
            p_save.setAttribute('style', 'color:gray; margin:3px');
            p_cancel.setAttribute('style', 'color:gray; margin:3px');
            p_edit.innerHTML = "edit";
            p_save.innerHTML = "save";
            p_cancel.innerHTML = "cancel";

            secondtext.setAttribute('class', 'hide');
            b_project.setAttribute('style', 'color:orange; font-weight:bold');
            b_project.innerHTML = result_sp[i]['project_name'];
            var projecttext = document.createElement('b');
            projecttext.setAttribute('style', 'color:black; font-weight:bold');
            projecttext.innerHTML = "Project: ";
            secondtext.appendChild(projecttext);
            secondtext.appendChild(b_project);
            secondtext.appendChild(p_edit);
            secondtext.appendChild(p_save);
            secondtext.appendChild(p_cancel);
            entry.appendChild(toptext);
            entry.appendChild(secondtext);

            var len_build = result_build.length;
            for(j = 0; j < len_build; j++){
                if(result_build[j]['sp_id_fk'] == result_sp[i]['id']){
                    var submenu = document.createElement('ol');
                    submenu.setAttribute('class', 'hide');
                    var bullet = document.createElement('span');
                    bullet.innerHTML = "- ";
                    submenu.appendChild(bullet);
                    var aTag2 = document.createElement('a');
                    aTag2.setAttribute('style', 'font-weight:bold');
                    aTag2.innerHTML = result_build[j]['name'];
                    submenu.appendChild(aTag2);
                    var edit = document.createElement('a');
                    var save = document.createElement('a');
                    var cancel = document.createElement('a');
		    edit.setAttribute('class', 'edit');
		    save.setAttribute('class', 'save');
		    cancel.setAttribute('class', 'cancel');
		    edit.setAttribute('style', 'color:gray; margin:3px');
		    save.setAttribute('style', 'color:gray; margin:3px');
		    cancel.setAttribute('style', 'color:gray; margin:3px');
		    edit.innerHTML = "edit";
                    save.innerHTML = "save";
                    cancel.innerHTML = "cancel";
                    var status_dot = document.createElement('span');
                    status_dot.innerHTML = "&#8226";
                    if(result_build[j]['status'] == 1 && result_build[j]['name'].indexOf('HQX.') == -1) {
                        status_dot.setAttribute('style', 'color:green; margin:3px');
                    }
		    else if(result_build[j]['name'].indexOf('HQX.') > -1) {
			if(result_build[j]['status'] == 1) {
			     status_dot.setAttribute('style', 'color:blue; margin:3px');
			}
			else if(result_build[j]['status'] == 2) {
			     status_dot.setAttribute('style', 'color:orange; margin:3px');
			}
			else if(result_build[j]['status'] == 3) {
			     status_dot.setAttribute('style', 'color:green; margin:3px');
			}
		    }
                    if(result_build[j]['status'] == 0) {
                        status_dot.setAttribute('style', 'color:red; margin:3px');
                    }
                    submenu.appendChild(status_dot);
                    submenu.appendChild(edit);
                    submenu.appendChild(save);
                    submenu.appendChild(cancel);
                    var wiki_b       = result_build[j]['wiki'];
                    var rno          = result_build[j]['release_note'];
                    var apps_id      = result_build[j]['apps_id'];
		    var gvm_id 	     = result_build[j]['gvm_id'];
                    var au_tag       = result_build[j]['au_tag'];
                    var release_date = result_build[j]['release_date'];

                    var information = [wiki_b, rno, apps_id, au_tag, release_date];
                    var lefts = ["Wiki ", "Release Note ", "APPS ID ", "AU Tag ", "Release Date "];
		    if(result_build[j]['name'].indexOf('HQX.') > -1) {
			information.splice(3, 0, gvm_id);
			lefts.splice(3, 0, "GVM ID "); 
		    }
                    var table = document.createElement('table');
                    table.setAttribute('class', 'hide');
                    table.setAttribute('style', 'border: 1px solid #444444; margin: 10px; width: 80%');
                    var tbody = document.createElement('tbody');
                    for(k = 0; k < information.length; k++) {
                        var tr = document.createElement('tr');
                        var lefttext = document.createElement('b');
                        var td_name = document.createElement('td');
                        var td_content = document.createElement('td');
                        tr.setAttribute('class', 'hidden_row');
                        tr.setAttribute('style', 'border: 1px solid #444444');
                        td_name.setAttribute('style', 'border: 1px solid #444444; width: 10%');
                        td_content.setAttribute('style', 'border: 1px solid #444444');
                        lefttext.innerHTML = lefts[k];
                        td_name.appendChild(lefttext);
                        if(k == 0) {
                            var link = document.createElement('a');
                            link.setAttribute('href', information[k]);
                            link.innerHTML = information[k];
                            td_content.appendChild(link);
                        }
			else if(k == 2 && (result_build[j]['status'] == 1 || result_build[j]['status'] == 3)) {
			    var link = document.createElement('a');
			    if(apps_id.indexOf('LV.') > -1 || apps_id.indexOf('QXA.') > -1) 
			        link.setAttribute('href', 'https://automotive-linux:7070/source/xref/' + information[k]);
			    else
				link.setAttribute('href', 'https://automotive-linux:7071/source/xref/' + information[k]);
			    link.innerHTML = information[k];
			    td_content.appendChild(link);
			}
			else if(k == 3 && result_build[j]['name'].indexOf('HQX.') > -1 && (result_build[j]['status'] == 2 || result_build[j]['status'] == 3)) {
			    var link = document.createElement('a');
			    if(gvm_id.indexOf('LV.') > -1) 
			        link.setAttribute('href', 'https://automotive-linux:7070/source/xref/' + information[k]);
			    else
				link.setAttribute('href', 'https://automotive-linux:7071/source/xref/' + information[k]);
			    link.innerHTML = information[k];
			    td_content.appendChild(link);

			}
			else {
                            var content = document.createElement('b');
                            content.innerHTML = information[k];
                            td_content.appendChild(content);
                        }	
			if(k == 1) {
			    var rn_button = document.createElement('img');
			    rn_button.setAttribute('type', 'image');
			    rn_button.setAttribute('src', 'offwhite/img/rn.png');	
			    rn_button.setAttribute('width', '25px');	
			    rn_button.setAttribute('height', '35px');
			    rn_button.setAttribute('style', 'border:0px; cursor:pointer; margin-left:10px; vertical-align:middle');
			    rn_button.setAttribute('onclick', 'open_releasenote(\'' + result_build[j]['name'] + '\',\'' + information[k]+'\')');
			    td_content.appendChild(rn_button);
			}
                        tr.appendChild(td_name);
                        tr.appendChild(td_content);
                        tbody.appendChild(tr);
		
                    }
                    table.appendChild(tbody);
                    submenu.appendChild(table);

                    entry.appendChild(submenu);
                }
            }
        }
        $(document).ready(function(){
            $(".menu>a").click(function(){
                var pointer = $(this).prev(".pointer");
                pointer.toggleClass('toggle-on');
                var submenu = $(this).nextAll("ol");
                var edit = submenu.children(".edit").first();
                var edit2 = submenu.children(".edit").eq(1);
                if( submenu.is(":visible") ){
                    submenu.slideUp();
                }else{
                    submenu.slideDown();
                    edit.show();
                    edit2.show();
                }
                table = $(this).nextAll("table");
                if( table.is(":visible") ) {
                    table.slideUp();
                }else{
                    table.slideDown();
                }
            });
            $(".hide>a").click(function(){
                if (this.innerHTML == 'edit' || this.innerHTML == 'save' || this.innerHTML == 'cancel'){
                        return;
                }
                var submenu = $(this).nextAll("ol");
                var edit = $(this).next().next().next(".edit");
                var save = edit.next(".save");
                var cancel = save.next(".cancel");

                if( submenu.is(":visible") ){
                    submenu.slideUp();
                }else{
                    submenu.slideDown();
                    edit.show();
                }
                var table = $(this).nextAll("table");
                if( table.is(":visible") ) {
                    table.slideUp();
                    edit.hide();
                    save.hide();
                    cancel.hide();
                }else{
                    table.slideDown();
                }
            });

            $(".edit").click(function(){
                // this is edit event
                var edit = $(this);
                var save = $(this).next(".save");
                var cancel = save.next(".cancel");
                var table = cancel.next("table");
                edit.hide();
                save.show();
                cancel.show();
                if(table.html() == null) {
                    var contents_wiki = $(this).prev();
                    var contentEditor =
                    '<input id="editbox" type="text" style="width:60%; height:60%" value=\"' + contents_wiki.html() + '\"/>'
                    contents_wiki.after(contentEditor);
                    contents_wiki.hide();
                }
                else {
                    var tbody = table.children();
                    var tr_wiki = tbody.children().eq(0);
                    var contents_wiki = tr_wiki.children().eq(1).children().eq(0);

                    var contentEditor =
                    '<td style="border: 1px solid #444444">' +
                    '    <input id="editbox" type="text" style="width:100%; height:100%" value=\"' + contents_wiki.html() + '\"/>'
                    '</td>';
                    var prev_td = tr_wiki.children().eq(1);
                    prev_td.after(contentEditor);
                    //prev_td.remove();
                    prev_td.hide();
                }
                document.getElementById('editbox').focus();

            });
            $(".save").click(function(){
                var save = $(this);
                var cancel = save.next(".cancel");
                var edit = save.prev(".edit");
                save.hide();
                cancel.hide();
                edit.show();
                var query = "";
                var table = cancel.next("table");
                if(table.html() == null) {
                    var after_value = document.getElementById('editbox').value;
                    if(after_value.match(/http/)) {
                        var name = $(this).parent().prev().html();
                        var contentEditor =
                        '<a href=\"' + after_value + '\" style="color:blue; font-weight:bold">' + after_value + '</a>';
                        query = "UPDATE sp SET wiki = \"" + after_value + "\" WHERE NAME = \"" + name + "\"";
			var id;
		    	for(var h = 0; h < result_sp.length; h++){
			    if(result_sp[h]['name'] === $(this).parent().prev().html()) {
				id = result_sp[h]['id'];
				result_sp[h]['wiki'] = after_value;
				request = $.ajax({
				    url: "https://automotive-linux:9999/db/sp/"+ id +"/",
				    type: "PUT",
				    contentType: 'application/json; charset=utf-8',
				    datatype: "json",
				    async: true,
				    data: JSON.stringify(result_sp[h]),
				    error: function(err) {
					console.log(err);
				    }
		    		});
				break;
			    }
		        }
                    }
                    else {
                        var name = $(this).parent().prev().prev().html();
                        var contentEditor =
                        '<b style=\"color:orange; font-weight:bold\">' + after_value + '</b>';
			var id;
		    	for(var h = 0; h < result_sp.length; h++){
			    if(result_sp[h]['name'] === $(this).parent().prev().prev().html()) {
				id = result_sp[h]['id'];
				result_sp[h]['project_name'] = after_value;
				request = $.ajax({
				    url: "https://automotive-linux:9999/db/sp/"+ id +"/",
				    type: "PUT",
				    contentType: 'application/json; charset=utf-8',
				    datatype: "json",
				    async: true,
				    data: JSON.stringify(result_sp[h]),
				    error: function(err) {
					console.log(err);
				    }
		    		});
				break;
			    }
		        }

                    }
                    var prev_wiki = $(this).prev().prev().prev();
                    var edit_wiki = $(this).prev().prev();

                    edit_wiki.after(contentEditor);
                    prev_wiki.remove();
                    edit_wiki.remove();
		    		   
                }
                else {
                    var name = $(this).prev().prev().html();
                    var tbody = table.children();
                    var tr_wiki = tbody.children().eq(0);
                    var after_value = document.getElementById('editbox').value;
                    var contentEditor =
                    '<td style="border: 1px solid #444444">' +
                    '    <a href=\"'+ after_value +'\">'+ after_value +'</a>';
                    '</td>';
                    query = "UPDATE build SET wiki = \"" + after_value + "\" WHERE NAME = \"" + name + "\"";
                    var edit_td = tr_wiki.children().eq(2);
                    var prev_td = tr_wiki.children().eq(1);
                    prev_td.after(contentEditor);
                    edit_td.remove();
                    prev_td.remove();
		    var id;
		    for(var h = 0; h < result_build.length; h++){
			if(result_build[h]['name'] === $(this).prev().prev().html()) {
				id = result_build[h]['id'];
				result_build[h]['wiki'] = after_value;
				request = $.ajax({
				    url: "https://automotive-linux:9999/db/build/"+ id +"/",
				    type: "PUT",
				    contentType: 'application/json; charset=utf-8',
				    datatype: "json",
				    async: true,
				    data: JSON.stringify(result_build[h]),
				    error: function(err) {
					console.log(err);
				    }
		    		});
				break;
			}
		    }

                }
		
		request = $.ajax({
	    	    url: "https://automotive-linux:9999/db/sp/",
		    type: "GET",
		    datatype: "json",
		    success: reqGetResponseSP
		});
            });
            $(".cancel").click(function(){
                var cancel = $(this);
                var save = cancel.prev(".save");
                var edit = save.prev(".edit");
                cancel.hide();
                save.hide();
                edit.show();

                var table = cancel.next("table");
                if(table.html() == null) {
                    var prev_wiki = $(this).prev().prev().prev().prev();
                    var edit_wiki = $(this).prev().prev().prev();
                    prev_wiki.show();
                    edit_wiki.remove();
                }
                else {
                    var tbody = table.children();
                    var tr_wiki = tbody.children().eq(0);
                    var edit_td = tr_wiki.children().eq(2);
                    var prev_td = tr_wiki.children().eq(1);
                    prev_td.show();
                    edit_td.remove();
                }
            });
            $('#editbox').live('keyup', function(e) {
                if(e.keyCode === 13) {
                    var save = $(e.target).closest('ol').children('.save');
                    save.trigger("click");
                }
                if(e.keyCode === 27) {
                    var cancel = $(e.target).closest('ol').children('.cancel');
                    cancel.trigger("click");
                }
            });
            $('.pointer').click(function() {

            });
        });
}
