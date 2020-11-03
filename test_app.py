import unittest

from app import merge_entries_by_date, merge_entries
from clockify import ClockifyDay


class AppTestCase(unittest.TestCase):
    def test_merge_entries_by_date(self):
        entries = [
            {'id': '5f9b189d57a1c13ad03da86b', 'description': 'XXXXX-001', 'timeInterval': {'start': '2020-10-30T19:31:41Z', 'end': '2020-10-29T20:23:41Z', 'duration': 'PT52M'}},
            {'id': '5f9b169457a1c13ad03da203', 'description': 'XXXXX-002', 'timeInterval': {'start': '2020-10-29T19:23:00Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT15M'}},
            {'id': '5f9af4ac1b69c27d161c9648', 'description': 'XXXXX-001', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT2H38M'}},
            {'id': '5f9aec083a1dc508bba4c4c8', 'description': 'XXXXX-003', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT1H'}},
            {'id': '5f9a9e911f3eb40b66a0c789', 'description': 'XXXXX-001', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT4H54M'}},
            {'id': '5f9a9514e16a5c5558331eda', 'description': 'XXXXX-004', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT30M'}},
            {'id': '5f9bf0671b69c27d1620a2cc', 'description': 'XXXXX-001', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT42M'}},
            {'id': '5f9bf0843a1dc508bba928e3', 'description': 'XXXXX-005', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT15M'}},
            {'id': '5f99a0cf1f3eb40b669c4474', 'description': 'XXXXX-006', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT15M'}},
            {'id': '5f9a77ea1f3eb40b669ea95d', 'description': 'XXXXX-001', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT54M'}},
        ]
        merged_entries = merge_entries_by_date(entries)
        self.assertEqual(len(merged_entries), 2)
        self.assertEqual(merged_entries[0].date, '2020-10-29')
        self.assertEqual(merged_entries[1].date, '2020-10-30')

    def test_merge_entries(self):
        entries = [
            {'id': '5f9b189d57a1c13ad03da86b', 'description': 'XXXXX-001', 'timeInterval': {'start': '2020-10-30T19:31:41Z', 'end': '2020-10-29T20:23:41Z', 'duration': 'PT52M'}},
            {'id': '5f9b169457a1c13ad03da203', 'description': 'XXXXX-002', 'timeInterval': {'start': '2020-10-29T19:23:00Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT15M'}},
            {'id': '5f9af4ac1b69c27d161c9648', 'description': 'XXXXX-001', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT2H38M'}},
            {'id': '5f9aec083a1dc508bba4c4c8', 'description': 'XXXXX-003', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT1H'}},
            {'id': '5f9a9e911f3eb40b66a0c789', 'description': 'XXXXX-001', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT4H54M'}},
            {'id': '5f9a9514e16a5c5558331eda', 'description': 'XXXXX-004', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT30M'}},
            {'id': '5f9bf0671b69c27d1620a2cc', 'description': 'XXXXX-001', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT42M'}},
            {'id': '5f9bf0843a1dc508bba928e3', 'description': 'XXXXX-005', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT15M'}},
            {'id': '5f99a0cf1f3eb40b669c4474', 'description': 'XXXXX-006', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT15M'}},
            {'id': '5f9a77ea1f3eb40b669ea95d', 'description': 'XXXXX-001', 'timeInterval': {'start': '2020-10-29T16:58:20Z', 'end': '2020-10-29T19:38:00Z', 'duration': 'PT54M'}},
        ]
        entries_by_date = [ClockifyDay('2020-10-29'), ClockifyDay('2020-10-30')]
        merged_entries = merge_entries(entries, entries_by_date)
        self.assertEqual(len(merged_entries), 2)
        self.assertEqual(merged_entries[0].date, '2020-10-29')
        self.assertEqual(merged_entries[1].date, '2020-10-30')
        self.assertEqual(len(merged_entries[0].entries), 6)
        self.assertEqual(len(merged_entries[1].entries), 1)

        self.assertEqual(merged_entries[0].entries[0].description, 'XXXXX-002')
        self.assertEqual(merged_entries[0].entries[0].hours, 0)
        self.assertEqual(merged_entries[0].entries[0].minutes, 15)
        self.assertListEqual(list(merged_entries[0].entries[0].ids.keys()), ['5f9b169457a1c13ad03da203'])

        self.assertEqual(merged_entries[0].entries[1].description, 'XXXXX-001')
        self.assertEqual(merged_entries[0].entries[1].hours, 9)
        self.assertEqual(merged_entries[0].entries[1].minutes, 8)
        self.assertListEqual(list(merged_entries[0].entries[1].ids.keys()), ['5f9af4ac1b69c27d161c9648', '5f9a9e911f3eb40b66a0c789', '5f9bf0671b69c27d1620a2cc', '5f9a77ea1f3eb40b669ea95d'])

        self.assertEqual(merged_entries[0].entries[2].description, 'XXXXX-003')
        self.assertEqual(merged_entries[0].entries[2].hours, 1)
        self.assertEqual(merged_entries[0].entries[2].minutes, 0)
        self.assertListEqual(list(merged_entries[0].entries[2].ids.keys()), ['5f9aec083a1dc508bba4c4c8'])

        self.assertEqual(merged_entries[0].entries[3].description, 'XXXXX-004')
        self.assertEqual(merged_entries[0].entries[3].hours, 0)
        self.assertEqual(merged_entries[0].entries[3].minutes, 30)
        self.assertListEqual(list(merged_entries[0].entries[3].ids.keys()), ['5f9a9514e16a5c5558331eda'])

        self.assertEqual(merged_entries[0].entries[4].description, 'XXXXX-005')
        self.assertEqual(merged_entries[0].entries[4].hours, 0)
        self.assertEqual(merged_entries[0].entries[4].minutes, 15)
        self.assertListEqual(list(merged_entries[0].entries[4].ids.keys()), ['5f9bf0843a1dc508bba928e3'])

        self.assertEqual(merged_entries[0].entries[5].description, 'XXXXX-006')
        self.assertEqual(merged_entries[0].entries[5].hours, 0)
        self.assertEqual(merged_entries[0].entries[5].minutes, 15)
        self.assertListEqual(list(merged_entries[0].entries[5].ids.keys()), ['5f99a0cf1f3eb40b669c4474'])

        self.assertEqual(merged_entries[1].entries[0].description, 'XXXXX-001')
        self.assertEqual(merged_entries[1].entries[0].hours, 0)
        self.assertEqual(merged_entries[1].entries[0].minutes, 52)
        self.assertListEqual(list(merged_entries[1].entries[0].ids.keys()), ['5f9b189d57a1c13ad03da86b'])


if __name__ == '__main__':
    unittest.main()
