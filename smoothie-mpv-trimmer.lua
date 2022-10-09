
local dur = 2500
    -- Duration of message, in milliseconds,
    -- feel free to lower it if you got that muscle memory uk what im sayin



local verbose = false
local mp = require 'mp'
local msg = require 'mp.msg'
local utils = require 'mp.utils'
local options = require 'mp.options'

Osdwarn = false
Trs = {} -- Creates a fresh empty table
Index = 1 -- Selects the trim 1, for it to be increased/decreased later
local direcseparator = package.config:sub(1, 1) -- Returns / on *nix and \ on Windows

local function notify(duration, ...)
	local args = {...}
	local text = ""

	for i, v in ipairs(args) do
		text = text .. tostring(v)
	end

    if text == nil then
        return
    end

    print(text)
	mp.command(string.format("show-text \"%s\" %d 1", text, duration))
end

local function create_chapter()
    local time_pos = mp.get_property_number("time-pos")
    local time_pos_osd = mp.get_property_osd("playback-time/full")
    local curr_chapter = mp.get_property_number("chapter")
    local chapter_count = mp.get_property_number("chapter-list/count")
    local all_chapters = mp.get_property_native("chapter-list")
    --mp.osd_message(time_pos_osd, 1)

    if chapter_count == 0 then
        all_chapters[1] = {
            title = "chapter_1",
            time = time_pos
        }
        curr_chapter = 0
    else
        for i = chapter_count, curr_chapter + 2, -1 do
            all_chapters[i + 1] = all_chapters[i]
        end
        all_chapters[curr_chapter+2] = {
            title = "chapter_"..curr_chapter,
            time = time_pos
        }
    end
    mp.set_property_native("chapter-list", all_chapters)
    mp.set_property_number("chapter", curr_chapter+1)
end

mp.add_key_binding("n", "ddqd", create_chapter)


local function incrIndex()

    if #Trs < 2 and Trs[Index+1] == nil then
        notify(dur, "You only have one starter index,\nstart making a second index before cycling through them.")
        return
    end

    if Trs[Index+1] == nil then
        Index = 1 -- Looping through
        notify(dur, "[c] (Looping) Increased index back down to ".. Index)
    else
        Index = Index + 1
        notify(dur, "[C] Increased index to ".. Index)
    end
end;mp.add_key_binding("C", "increase-index", incrIndex)


local function decrIndex()
    if #Trs < 2 then
        notify(dur, "You only have one starter index,\nstart making a second index before cycling through them.")
        return
    end

    if Trs[Index - 1] == nil then
        Index = #Trs -- Looping through
        notify(dur, "[c] (Looping) Lowered index back up to ".. Index)
    else
        Index = Index - 1
        notify(dur, "[c] Lowered index to ".. Index)
    end
end;mp.add_key_binding("c", "decrease-index", decrIndex)


local function showPoints()
    local fps = mp.get_property('container-fps')
    print(utils.format_json(Trs))
    msg = "Trimming points:"
    if #Trs > 11 and Osdwarn == false  then
        notify(dur, "You have too much trimming points\n for it to fit on the OSD, check the console.")
        Osdwarn = true
        return
        elseif #Trs > 11 and Osdwarn == true then
            return
    end
    for ind, _ in ipairs(Trs) do
        if Trs[ind].filename ~= nil then
            msg = msg .. "\n" .. "[" .. ind .. "] " .. Trs[ind].filename
        end
        if Trs[ind].start ~= nil then
            msg = msg .. " : " .. string.sub(string.format(Trs[ind].start/fps), 1, 4)
        end
        if Trs[ind].fin ~= nil then
            msg = msg .. " - " .. string.sub(string.format(Trs[ind].fin/fps), 1, 4)
        end
    end
    print(msg)
    mp.osd_message(msg, dur/500) -- 2x longer than normal dur, divide by / 1000 for same length
end;mp.add_key_binding("Ctrl+p", "showPoints", showPoints)


local function getIndex()
    notify(dur, "[g] Selected index is ".. Index)
end;mp.add_key_binding("Ctrl+g", "get-index", getIndex)

local function start()
    local pos = mp.get_property_number('playback-time/full')
    local fn = mp.get_property("stream-open-filename")
    local curframe = mp.get_property_number('estimated-frame-number')

    if string.match(fn,direcseparator) == nil then -- If running on command line stuff like 'mpv *.mp4' it doesn't provide full path
        fn = mp.get_property("working-directory")..direcseparator..fn
    end

    if Trs[Index] == nil then Trs[Index] = {} end
    Trs[Index]['start'] = curframe
    Trs[Index]['filename'] = fn

    notify(dur, "[g] Set start point of index ["..Index.."] at ".. pos)

    create_chapter()

end;mp.add_key_binding("g", "set-start", start)


local function sof()
    notify(dur, "[S] Setting index " .. Index .. " to 00:00:00 (start of file)")
    if Trs[Index] == nil then Trs[Index] = {} end
    Trs[Index]['start'] = 0
end;mp.add_key_binding("G", "set-sof", sof)


local function fin()
    local pos = mp.get_property_number('playback-time/full')
    local fn = mp.get_property("stream-open-filename")
    local curframe = mp.get_property_number('estimated-frame-number')
    if Trs[Index] == nil then Trs[Index] = {} end
    Trs[Index]['fin'] = curframe
    if string.match(fn,direcseparator) == nil then -- If running on command line stuff like *.mp4 it doesn't provide full path
        fn = mp.get_property("working-directory")..direcseparator..fn
    end

    if Trs[Index]['start'] == nil then
        notify(dur, "[g] You need to set a start point first.")
        return nil
    end

    Trs[Index]['filename'] = fn

    notify(dur, "[h] Set end point of index ["..Index.."] at ".. pos)

    if Trs[Index + 1] == nil then Trs[Index + 1] = {} end
    if Trs[Index + 1]['start'] == nil and Trs[Index + 1]['fin'] == nil then -- Only step up if it's the last index
        Index = Index + 1                                                   -- Else it means the user has went back down on an older index
    end

    create_chapter()

end;mp.add_key_binding("h", "set-fin", fin)

local function eof()

    if Trs[Index]['start'] == nil then
        notify(dur, "[g] You need to set a start point first.")
        return
    end

    local framecount = mp.get_property('estimated-frame-count')
    notify(dur, "[H] Set end point of index ["..Index.."] to ".. framecount .. " (End of file)")
    Trs[Index]['fin'] = framecount
end;mp.add_key_binding("H", "set-eof", eof)

local function render()
    Trs[#Trs] = nil -- beautiful syntax to remove last object
    Cmd = {args={'sm','-trim', utils.format_json(Trs)}}
    if verbose == true then
        table.insert(Cmd.args,'-verbose')
        command = ''
        for v, k in pairs(Cmd.args) do -- awful for loop to join array to string
            command = command .. k .. ' '
        end
        print('COMMAND: ' .. command)
    end
    utils.subprocess_detached(Cmd)
    mp.commandv('quit')
end;mp.add_key_binding("Ctrl+r", "sm-render", render)

local function toggleVerb()
    if verbose == true then
        notify(dur, "[Ctrl+v] toggled off Verbose")
        verbose = false
    elseif verbose == false then
        notify(dur, "[Ctrl+v] toggled on Verbose")
        verbose = true
    end
end;mp.add_key_binding("Ctrl+v", "smt-toggle-verbose", toggleVerb)
