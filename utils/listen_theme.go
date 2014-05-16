/**
 * Copyright (c) 2011 ~ 2014 Deepin, Inc.
 *               2013 ~ 2014 jouyouyun
 *
 * Author:      jouyouyun <jouyouwen717@gmail.com>
 * Maintainer:  jouyouyun <jouyouwen717@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, see <http://www.gnu.org/licenses/>.
 **/

package main

import (
	xs "dbus/com/deepin/sessionmanager"
	"dlib/gio-2.0"
	"dlib/utils"
	"fmt"
	"github.com/howeyc/fsnotify"
	"os"
	"path"
	"regexp"
)

var (
	themeName     = "Deepin"
	xsObj         *xs.XSettings
	watchObj      *fsnotify.Watcher
	utilObj       = utils.NewUtils()
	wmSettings    = gio.NewSettings("org.gnome.desktop.wm.preferences")
	prevWatchDirs []string
)

func cancelWatchDirs() {
	if watchObj == nil {
		return
	}

	for _, dir := range prevWatchDirs {
		watchObj.RemoveWatch(dir)
	}
}

func watchDirs() {
	if watchObj == nil {
		var err error
		if watchObj, err = fsnotify.NewWatcher(); err != nil {
			return
		}
	}

	homeDir, ok := utilObj.GetHomeDir()
	if !ok {
		fmt.Println("Get Home Dir Failed")
		panic("Get Home Dir Failed")
	}
	dirs := getAllDirName(path.Join(homeDir, ".themes"))
	prevWatchDirs = dirs
	for _, dir := range dirs {
		watchObj.Watch(dir)
	}

}

func handleEvent() {
	for {
		select {
		case ev := <-watchObj.Event:
			if ev == nil {
				break
			}
			if ok, _ := regexp.MatchString(`\.swa?px?$`, ev.Name); ok {
				break
			}
			fmt.Println("Event: ", ev)
			xsObj.SetString("Net/ThemeName", themeName)
			wmSettings.SetString("theme", themeName)
			if ev.IsCreate() || ev.IsDelete() {
				cancelWatchDirs()
				watchDirs()
			}
		}
	}
}

func getAllDirName(dir string) []string {
	f, err := os.Open(dir)
	if err != nil {
		fmt.Printf("Open '%s' failed: %v\n", dir, err)
		return []string{}
	}
	defer f.Close()

	finfos, err1 := f.Readdir(0)
	if err1 != nil {
		fmt.Printf("Readdir '%s' failed: %v\n", dir, err1)
		return []string{}
	}

	dirs := []string{}
	dirs = append(dirs, dir)
	for _, info := range finfos {
		if info == nil || !info.IsDir() {
			continue
		}

		tmp := getAllDirName(path.Join(dir, info.Name()))
		dirs = append(dirs, tmp...)
	}

	return dirs
}

func main() {
	if len(os.Args) == 2 {
		themeName = os.Args[1]
	}
	var err error

	xsObj, err = xs.NewXSettings("com.deepin.SessionManager",
		"/com/deepin/XSettings")
	if err != nil {
		fmt.Println("New XSettings Failed: ", err)
		return
	}
	watchObj, err = fsnotify.NewWatcher()
	if err != nil {
		fmt.Println("New Watch Failed: ", err)
		return
	}

	watchDirs()
	handleEvent()
}
