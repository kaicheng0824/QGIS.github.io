import getLMP
import getNodeMetadata
import processLMP
import csvToGeoJSON

if __name__ == "__main__":
    getNodeMetadata.main()
    getLMP.main()
    processLMP.main()
    csvToGeoJSON.main()