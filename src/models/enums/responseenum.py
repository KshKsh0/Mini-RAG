from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS='File_validated_successfully'
    FILE_TYPE_NOT_SUPPORTED ='File_type_not_supported'
    FILE_SIZE_EXCEEDED = 'File_size_exceeded'
    FILE_UPLOAD_SUCCESS = 'File_upload_success'
    FILE_UPLOAD_FAILED = 'File_upload_failed'
    PROCESSING_FAILED  = 'processing_failed'
    PROCESSING_SUCCESS  = 'processing_success'
    NO_FILES_ERROR = 'not_found_file'
    FILE_ID_ERROR = 'no_file_id_found'
    PROJCT_NOT_FOUND_ERROR = 'projct_not_found'
    INSERTED_TO_VECTOR_DB_ERROR = 'insertion_to_vectorDB_error'
    INSERTED_TO_VECTOR_DB_SUCCESS = 'insertion_to_vectorDB_success'
    VECTOR_COLLECTION_RETRIVED = 'vectordb_collectoin_retrieved'
    VECTOR_SEARCH_DONE = 'vectordb_search_done'
