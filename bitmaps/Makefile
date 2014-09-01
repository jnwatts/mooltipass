BUNDLE ?= ./bundle.py
RESOURCE ?= ./resource.py
BITMAP ?= ./bitmap.py

# Extract list of image/font files from resources.yaml
RESOURCES = $(shell $(RESOURCE) -d resources.yaml)

all: bundle.img file_ids.h

# Rebuild .img file if corresponding .h file is newer
%.img: %.h
	$(BITMAP) -i $< -o $@ -c -n $(@:.img=)

# Rebuild bundle if either resources.yaml or any named resource changes
bundle.img: resources.yaml $(RESOURCES)
	$(BUNDLE) -cf $@ $<

# Rebuild file_ids.h if resources.yaml changes
file_ids.h: resources.yaml
	cat file_ids_header.h > file_ids.h
	$(BUNDLE) -ef - $< >> file_ids.h
	cat file_ids_footer.h >> file_ids.h

clean:
	rm -f bundle.img
	rm -f file_ids.h

