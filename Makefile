BUILDCONF=hack/config

debian:
    (cd src/; dpkg-buildpackage)
    
upload-controller: out
    hack/upload.sh controller $(BUILDCONF)
    
upload-nodes: out
    hack/upload.sh nodes $(BUILDCONF)
    
test: out
    hack/upload.sh controller $(BUILDCONF)
    hack/upload.sh nodes $(BUILDCONF)
    hack/test.sh $(BUILDCONF)
    
all: debian
    
clean:
    rm -rf out
    
out:
    mkdir out
    touch out/.created