#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

all: check


check:
	python3 -m testtools.run wikkid.tests.test_suite


clean:
	@find . -name '*.py[co]' -print0 | xargs -r0 $(RM)
	@find . -name '*~' -print0 | xargs -r0 $(RM)


.PHONY: check clean

docker:
	docker build -t ghcr.io/wikkid-team/wikkid .
	docker push ghcr.io/wikkid-team/wikkid
