#!/bin/bash
################################################################################
##
## Copyright 2006 - 2017, Paul Beckingham, Federico Hernandez.
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included
## in all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
## OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
## THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.
##
## http://www.opensource.org/licenses/mit-license.php
##
################################################################################

# Warn that this is not a quick report.
echo 'Finding most urgent tasks in each project...'

# Tags to exclude. WAITING is Taskwarrior's virtual tag for waiting tasks.
EXCLUDE="-someday -inbox -WAITING -birthday -waiting"

# UUIDS is a string that will contain the UUID of every task we wish to see.
UUIDS=

# Enumerate pending task UUIDs having no project, minus the excluded ones.
for uuid in $(task status:pending project: $EXCLUDE _uuids)
do
  UUIDS="$UUIDS $uuid"
done

# Enumerate the project names for all active projects.
for project in $(task rc.list.all.projects=0 _projects)
do
  # Temporarily override the 'next' report output to yield only UUID, and only
  # one task. The exclusions are part of the filter, so the "most urgent" task
  # is chosen from what remains rather than being dropped afterwards.
  uuid=$(task project:"$project" $EXCLUDE rc.verbose=nothing \
         rc.report.next.columns=uuid rc.report.next.labels=uuid limit:1 next)
  UUIDS="$UUIDS $uuid"
done

# Run the next report, showing only the specific list of tasks.
# Guard: with no UUIDs, `task next` would show everything.
if [ -z "${UUIDS// /}" ]; then
  echo "No matching tasks."
else
  task $UUIDS next
fi
