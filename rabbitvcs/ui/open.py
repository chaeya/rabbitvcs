#
# This is an extension to the Nautilus file manager to allow better 
# integration with the Subversion source control system.
# 
# Copyright (C) 2006-2008 by Jason Field <jason@jasonfield.com>
# Copyright (C) 2007-2008 by Bruce van der Kooij <brucevdkooij@gmail.com>
# Copyright (C) 2008-2008 by Adam Plumb <adamplumb@gmail.com>
# 
# RabbitVCS is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# RabbitVCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with RabbitVCS;  If not, see <http://www.gnu.org/licenses/>.
#

from os import getcwd
import os.path

import pygtk
import gobject
import gtk

from rabbitvcs.ui import InterfaceNonView
from rabbitvcs.ui.action import SVNAction, GitAction

import rabbitvcs.vcs

from rabbitvcs import gettext
_ = gettext.gettext

class SVNOpen(InterfaceNonView):
    """
    This class provides a handler to open tracked files.
    
    """

    def __init__(self, path, revision):
        """
        @type   path: string
        @param  path: The path to open
        
        @type   revision: string
        @param  revision: The revision of the file to open
        
        """
        
        InterfaceNonView.__init__(self)

        self.vcs = rabbitvcs.vcs.VCS()
        self.svn = self.vcs.svn()

        if not revision:
            revision = "HEAD"

        revision_obj = self.svn.revision("number", number=revision)

        url = self.svn.get_repo_root_url(path) + '/' + path
        dest = "/tmp/rabbitvcs-" + revision + "-" + os.path.basename(path)
        
        self.svn.export(
            url,
            dest,
            revision=revision_obj
        )
        
        rabbitvcs.util.helper.open_item(dest)

        raise SystemExit()

class GitOpen(InterfaceNonView):
    """
    This class provides a handler to open tracked files.
    
    """

    def __init__(self, path, revision):
        """
        @type   path: string
        @param  path: The path to open
        
        @type   revision: string
        @param  revision: The revision of the file to open
        
        """
        
        InterfaceNonView.__init__(self)

        self.vcs = rabbitvcs.vcs.VCS()
        self.git = self.vcs.git(path)

        if not revision:
            revision = "HEAD"

        revision_obj = self.git.revision(revision)

        dest_dir = "/tmp/rabbitvcs-" + unicode(revision)
        
        self.git.export(
            path,
            dest_dir,
            revision=revision_obj
        )
        
        dest_path = "%s/%s" % (dest_dir, os.path.basename(path))
        
        rabbitvcs.util.helper.open_item(dest_path)

        raise SystemExit()

classes_map = {
    rabbitvcs.vcs.VCS_SVN: SVNOpen,
    rabbitvcs.vcs.VCS_GIT: GitOpen
}

def open_factory(path, revision):
    guess = rabbitvcs.vcs.guess(path)
    return classes_map[guess["vcs"]](path, revision)

if __name__ == "__main__":
    from rabbitvcs.ui import main, REVISION_OPT
    (options, paths) = main(
        [REVISION_OPT],
        usage="Usage: rabbitvcs open path [-r REVISION]"
    )
    
    window = open_factory(paths[0], options.revision)
    window.register_gtk_quit()
    gtk.main()