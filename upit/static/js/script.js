/**
* UpIt - Fileupload
*
* Copyright (C) 2011 Bernhard Posselt, bernhard.posselt@gmx.at
*
* UpIt is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 3 of the License, or
* (at your option) any later version.
*
* UpIt is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
*
*/

$(document).ready(function() {
    /**
     * Slideup login
     */
    $(".login").fadeIn("fast");
     
    prettyPrint();
     
    /**
     * Autocopy to clipboard on hover
     */
    $(".file_item").mouseover(function(){
        // fade in info panel
        if($(".clipboard_field").css("display") === "none"){
            $(".clipboard_field").slideDown("fast");
        }
        
        
        var cp_link = $(this).children("a").attr("href");
        cp_link = window.location.protocol + "//" + window.location.host + cp_link;
        $(".clipboard_field").html(cp_link);
        return false;
    });
});

