from flask import jsonify
import logging

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

def handle_errors(app):
    @app.errorhandler(400)
    def bad_request(error):
        logger.error(f'Bad request: {error}')
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal error: {error}')
        return jsonify({'error': 'Internal server error'}), 500