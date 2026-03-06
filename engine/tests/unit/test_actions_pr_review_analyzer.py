"""Unit tests for PR Review Analyzer action."""

import pytest

from codeflow_engine.actions.pr_review_analyzer import (
    PRReviewAnalysis,
    PRReviewAnalyzer,
)


class TestPRReviewAnalysis:
    """Test suite for PRReviewAnalysis dataclass."""

    def test_analysis_creation(self):
        """Test creating PRReviewAnalysis."""
        analysis = PRReviewAnalysis(
            pr_number=123,
            review_count=3,
            comment_count=10,
            approval_count=2,
            requested_changes_count=1,
            review_comment_count=8,
            review_commenters=["user1", "user2"],
        )
        assert analysis.pr_number == 123
        assert analysis.review_count == 3
        assert analysis.approval_count == 2
        assert len(analysis.review_commenters) == 2

    def test_analysis_optional_fields(self):
        """Test PRReviewAnalysis with optional fields."""
        analysis = PRReviewAnalysis(
            pr_number=123,
            review_count=1,
            comment_count=0,
            approval_count=1,
            requested_changes_count=0,
            review_comment_count=0,
            review_commenters=[],
            review_duration_hours=24.5,
            sentiment_score=0.8,
            risk_score=0.2,
            summary="Good PR",
            recommendations=["Merge"],
        )
        assert analysis.review_duration_hours == 24.5
        assert analysis.sentiment_score == 0.8
        assert analysis.summary == "Good PR"


class TestPRReviewAnalyzer:
    """Test suite for PRReviewAnalyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create a PRReviewAnalyzer instance."""
        return PRReviewAnalyzer()

    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer is not None
        assert analyzer.config == {}

    def test_analyzer_initialization_with_config(self):
        """Test analyzer initialization with config."""
        config = {"min_reviews": 2}
        analyzer = PRReviewAnalyzer(config=config)
        assert analyzer.config == config

    def test_analyze_reviews_basic(self, analyzer):
        """Test basic review analysis."""
        reviews_data = [
            {"state": "APPROVED", "user": {"login": "reviewer1"}},
            {"state": "APPROVED", "user": {"login": "reviewer2"}},
            {"state": "CHANGES_REQUESTED", "user": {"login": "reviewer1"}},
        ]
        
        comments_data = [
            {"user": {"login": "reviewer1"}, "body": "Looks good"},
            {"user": {"login": "reviewer2"}, "body": "Needs changes"},
        ]
        
        result = analyzer.analyze_reviews(123, reviews_data, comments_data)
        assert result.pr_number == 123
        assert result.review_count == 3
        assert result.approval_count == 2
        assert result.requested_changes_count == 1
        assert result.review_comment_count == 2
        assert len(result.review_commenters) == 2

    def test_analyze_reviews_no_reviews(self, analyzer):
        """Test analysis with no reviews."""
        result = analyzer.analyze_reviews(123, [], [])
        assert result.review_count == 0
        assert result.approval_count == 0
        assert result.comment_count == 0

    def test_analyze_reviews_with_pr_data(self, analyzer):
        """Test analysis with PR metadata."""
        reviews_data = [{"state": "APPROVED"}]
        comments_data = []
        pr_data = {
            "created_at": "2025-01-01T00:00:00Z",
            "merged_at": "2025-01-02T00:00:00Z",
        }
        
        result = analyzer.analyze_reviews(123, reviews_data, comments_data, pr_data)
        assert result.summary is not None
        assert result.recommendations is not None

    def test_generate_summary(self, analyzer):
        """Test summary generation."""
        analysis = PRReviewAnalysis(
            pr_number=123,
            review_count=2,
            comment_count=5,
            approval_count=2,
            requested_changes_count=0,
            review_comment_count=5,
            review_commenters=["user1"],
        )
        
        summary = analyzer._generate_summary(analysis)
        assert isinstance(summary, str)
        assert "PR #123" in summary
        assert "2 reviews" in summary or "2 approvals" in summary

    def test_generate_recommendations_approved(self, analyzer):
        """Test recommendation generation for approved PR."""
        analysis = PRReviewAnalysis(
            pr_number=123,
            review_count=2,
            comment_count=0,
            approval_count=2,
            requested_changes_count=0,
            review_comment_count=0,
            review_commenters=[],
        )
        
        recommendations = analyzer._generate_recommendations(analysis)
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0

    def test_generate_recommendations_changes_requested(self, analyzer):
        """Test recommendation generation for PR with requested changes."""
        analysis = PRReviewAnalysis(
            pr_number=123,
            review_count=1,
            comment_count=5,
            approval_count=0,
            requested_changes_count=1,
            review_comment_count=5,
            review_commenters=["reviewer1"],
        )
        
        recommendations = analyzer._generate_recommendations(analysis)
        assert isinstance(recommendations, list)
        # Should have recommendations about addressing feedback
        assert len(recommendations) > 0

    def test_generate_recommendations_no_reviews(self, analyzer):
        """Test recommendation generation for PR with no reviews."""
        analysis = PRReviewAnalysis(
            pr_number=123,
            review_count=0,
            comment_count=0,
            approval_count=0,
            requested_changes_count=0,
            review_comment_count=0,
            review_commenters=[],
        )
        
        recommendations = analyzer._generate_recommendations(analysis)
        assert isinstance(recommendations, list)
        # Should recommend getting reviews
        assert len(recommendations) > 0

